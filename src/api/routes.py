from fastapi import APIRouter, HTTPException, Depends
from src.agent.router import AgentRouter
from src.agent.engine import FinancialAgent
from src.guardrail.validator import GuardrailValidator
from src.tools.math_tool import MathTool
from src.api.schemas import (
    ChatMessageRequest,
    ChatMessageResponse,
    PendingAction,
    ReportData,
    ConfirmTransactionRequest,
    ConfirmTransactionResponse,
    FinancialSummaryResponse,
    TransactionItem,
)

router = APIRouter()
validator = GuardrailValidator()

def get_agent() -> AgentRouter:
    return AgentRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "app": "financeiro-api"}

@router.post("/api/chat", response_model=ChatMessageResponse)
def handle_chat(payload: ChatMessageRequest, agent = Depends(get_agent)):
    # 1. Validação de Guardrail
    guardrail_result = validator.validate(payload.message)
    if not guardrail_result.is_valid:
        return ChatMessageResponse(
            response=guardrail_result.message,
            pending_action=None,
            is_report=False,
            report_data=None,
            agent_name="guardrail"
        )

    # 2. Se o agente for uma instância de AgentRouter (roteamento multiagente nativo)
    if isinstance(agent, AgentRouter):
        from src.agent.base import AgentContext
        ctx = AgentContext(message=payload.message, history=payload.history or [])
        res = agent.route(ctx)
        
        pending_obj = PendingAction(**res.pending_transaction) if res.pending_transaction else None
        report_data_obj = ReportData(**res.report_data) if res.report_data else None
        is_report = report_data_obj is not None or (hasattr(agent, "is_report_request") and agent.is_report_request(payload.message))
        
        return ChatMessageResponse(
            response=res.reply,
            pending_action=pending_obj,
            is_report=is_report,
            report_data=report_data_obj,
            agent_name=res.agent_name,
            suggested_actions=res.suggested_actions or None
        )

    # 3. Fallback / Mock compatível com testes legados
    pending = agent.detect_mutation_intent(payload.message)
    if pending:
        desc = pending.get("descricao", "Registro")
        val = pending.get("valor", 0.0)
        label = pending.get("action_label", "Adicionar")
        pending_obj = PendingAction(**pending)
        return ChatMessageResponse(
            response=f"📋 Deseja confirmar a seguinte ação?\n\n**Operação:** {label}\n**Descrição:** {desc}\n**Valor:** R$ {val:.2f}",
            pending_action=pending_obj,
            is_report=False,
            report_data=None,
            agent_name="transaction_agent"
        )

    is_report = agent.is_report_request(payload.message)
    report_data_obj = None
    if is_report:
        raw_rep = agent.generate_report_data()
        report_data_obj = ReportData(**raw_rep)

    agent_response = agent.process_message(payload.message, payload.history)
    return ChatMessageResponse(
        response=agent_response,
        pending_action=None,
        is_report=is_report,
        report_data=report_data_obj,
        agent_name="legacy_agent"
    )

@router.get("/api/transactions", response_model=FinancialSummaryResponse)
def get_transactions(agent: FinancialAgent = Depends(get_agent)):
    expenses = agent.expense_tool.list_all_expenses()
    incomes = agent.income_tool.service.get_incomes()

    tot_despesas = sum(MathTool.parse_float(e.get("Valor", 0)) for e in expenses)
    tot_receitas = sum(MathTool.parse_float(i.get("Valor", 0)) for i in incomes)
    saldo = tot_receitas - tot_despesas

    from src.tools.category import CategoryTool
    cat_dict = {}
    for e in expenses:
        cat = e.get("Categoria")
        if not cat or str(cat).strip().lower() in ["", "outros", "none", "geral"]:
            inferred = CategoryTool.categorize(e.get("Descrição", ""))
            cat = inferred if inferred else "Outros"
        val = MathTool.parse_float(e.get("Valor", 0))
        cat_dict[cat] = cat_dict.get(cat, 0.0) + val

    fixed_items = []
    for e in expenses:
        cat = e.get("Categoria")
        if not cat or str(cat).strip().lower() in ["", "outros", "none", "geral"]:
            cat = CategoryTool.categorize(e.get("Descrição", "")) or "Outros"
        fixed_items.append(
            TransactionItem(
                descricao=e.get("Descrição", "Sem descrição"),
                valor=MathTool.parse_float(e.get("Valor", 0)),
                tipo=e.get("Tipo", "fixa"),
                categoria=cat
            )
        )

    income_items = [
        TransactionItem(
            descricao=i.get("Descrição", "Sem descrição"),
            valor=MathTool.parse_float(i.get("Valor", 0)),
            tipo="receita"
        ) for i in incomes
    ]

    return FinancialSummaryResponse(
        total_receitas=round(tot_receitas, 2),
        total_despesas=round(tot_despesas, 2),
        saldo_liquido=round(saldo, 2),
        fixed_expenses=fixed_items,
        incomes=income_items,
        despesas_por_categoria={k: round(v, 2) for k, v in cat_dict.items()},
    )

@router.post("/api/transactions/confirm", response_model=ConfirmTransactionResponse)
def confirm_transaction(payload: ConfirmTransactionRequest, agent: FinancialAgent = Depends(get_agent)):
    try:
        result_msg = agent.execute_transaction(payload.model_dump())
        updated_report = ReportData(**agent.generate_report_data())
        return ConfirmTransactionResponse(
            success=True,
            message=result_msg,
            report_data=updated_report
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao confirmar transação: {str(e)}")

@router.get("/api/reports", response_model=ReportData)
def get_reports(agent: FinancialAgent = Depends(get_agent)):
    data = agent.generate_report_data()
    return ReportData(**data)
