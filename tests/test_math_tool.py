import pytest
from src.tools.math_tool import MathTool

def test_math_evaluate_simple():
    assert MathTool.evaluate("200 / 2") == 100.0
    assert MathTool.evaluate("150 * 3") == 450.0
    assert MathTool.evaluate("100 + 50 - 20") == 130.0

def test_math_divide():
    assert MathTool.divide(500, 2) == 250.0

def test_math_multiply():
    assert MathTool.multiply(150, 2) == 300.0

def test_math_divide_by_zero():
    with pytest.raises(ValueError):
        MathTool.divide(100, 0)
