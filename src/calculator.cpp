#include "calculator.h"
#include <cmath>
#include <stdexcept>

int Calculator::add(int a, int b)
{
    return a + b;
}

int Calculator::subtract(int a, int b)
{
    return a - b;
}

int Calculator::multiply(int a, int b)
{
    return a * b;
}

double Calculator::divide(double a, double b)
{
    if (b == 0.0)
    {
        throw std::invalid_argument("Division by zero");
    }
    return a / b;
}

int Calculator::power(int base, int exponent)
{
    if (exponent < 0)
    {
        throw std::invalid_argument("Negative exponent not supported");
    }

    int result = 1;
    for (int i = 0; i < exponent; ++i)
    {
        result *= base;
    }
    return result;
}

double Calculator::squareRoot(double number)
{
    if (number < 0)
    {
        throw std::invalid_argument("Square root of negative number");
    }
    return std::sqrt(number);
}

bool Calculator::isEven(int number)
{
    return number % 2 == 0;
}

int Calculator::factorial(int n)
{
    if (n < 0)
    {
        throw std::invalid_argument("Factorial of negative number");
    }
    return factorialHelper(n);
}

int Calculator::factorialHelper(int n)
{
    if (n <= 1)
    {
        return 1;
    }
    return n * factorialHelper(n - 1);
}