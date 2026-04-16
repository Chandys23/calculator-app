let expression = '';

function addToExpression(value) {
    expression += value;
    updateDisplay();
}

function addFunction(func) {
    expression += func + '(';
    updateDisplay();
}

function clearDisplay() {
    expression = '';
    updateDisplay();
}

function deleteLast() {
    expression = expression.slice(0, -1);
    updateDisplay();
}

function toggleSign() {
    if (expression) {
        if (expression.startsWith('-')) {
            expression = expression.slice(1);
        } else {
            expression = '-' + expression;
        }
        updateDisplay();
    }
}

function updateDisplay() {
    document.getElementById('expression').value = expression;
}

async function calculate() {
    if (!expression) return;
    
    try {
        const response = await fetch(`/api/calc?expression=${encodeURIComponent(expression)}`);
        const data = await response.json();
        
        if (data.error) {
            document.getElementById('result').textContent = 'Error: ' + data.error;
        } else {
            const result = parseFloat(data.result.toFixed(8));
            document.getElementById('result').textContent = result;
            expression = result.toString();
            document.getElementById('expression').value = '';
        }
    } catch (error) {
        document.getElementById('result').textContent = 'Connection Error';
    }
}

// Allow Enter key to calculate
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            calculate();
        }
    });
    
    // Handle number and operator keys
    document.addEventListener('keydown', function(event) {
        if (/^[0-9+\-*/.%]$/.test(event.key)) {
            addToExpression(event.key);
        } else if (event.key === 'Backspace') {
            deleteLast();
        } else if (event.key === 'Escape') {
            clearDisplay();
        }
    });
});