#pragma once

class Calculator
{
public:
    // Basic arithmetic operations
    int add(int a, int b);
    int subtract(int a, int b);
    int multiply(int a, int b);
    double divide(double a, double b);

    // Advanced operations
    int power(int base, int exponent);
    double squareRoot(double number);

    // Utility functions
    bool isEven(int number);
    int factorial(int n);

private:
    // Helper function for factorial calculation
    int factorialHelper(int n);
};