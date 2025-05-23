function solveEquation() {

    const x = 2;
    const y = 1;
    const b = 9;
            
    const numerator = 3 * x + 2 * y;
    const denominator = 5 * b;
    const Z = numerator / denominator;
            
    return Z.toFixed(4);
}
document.getElementById('answer').textContent = solveEquation()