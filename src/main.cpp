#include <iostream>
#include "calculator.h"
#include "string_utils.h"

int main()
{
    std::cout << "C++ Unit Test Generator - Sample Application\n";
    std::cout << "============================================\n\n";

    // Demonstrate Calculator functionality
    Calculator calc;

    std::cout << "Calculator Demo:\n";
    std::cout << "2 + 3 = " << calc.add(2, 3) << "\n";
    std::cout << "10 - 4 = " << calc.subtract(10, 4) << "\n";
    std::cout << "5 * 6 = " << calc.multiply(5, 6) << "\n";
    std::cout << "15 / 3 = " << calc.divide(15, 3) << "\n";
    std::cout << "2^8 = " << calc.power(2, 8) << "\n";
    std::cout << "sqrt(16) = " << calc.squareRoot(16) << "\n";
    std::cout << "Is 4 even? " << (calc.isEven(4) ? "Yes" : "No") << "\n";
    std::cout << "5! = " << calc.factorial(5) << "\n\n";

    // Demonstrate StringUtils functionality
    std::cout << "String Utils Demo:\n";
    std::string test_string = "Hello World";

    std::cout << "Original: " << test_string << "\n";
    std::cout << "Reversed: " << StringUtils::reverse(test_string) << "\n";
    std::cout << "Uppercase: " << StringUtils::toUpperCase(test_string) << "\n";
    std::cout << "Lowercase: " << StringUtils::toLowerCase(test_string) << "\n";
    std::cout << "Vowels count: " << StringUtils::countVowels(test_string) << "\n";
    std::cout << "Word count: " << StringUtils::countWords(test_string) << "\n";

    std::string palindrome = "racecar";
    std::cout << "Is '" << palindrome << "' a palindrome? "
              << (StringUtils::isPalindrome(palindrome) ? "Yes" : "No") << "\n";

    std::string email = "test@example.com";
    std::cout << "Is '" << email << "' a valid email? "
              << (StringUtils::isValidEmail(email) ? "Yes" : "No") << "\n";

    std::cout << "\nThis application demonstrates various C++ features that can be tested\n";
    std::cout << "using the AI-powered unit test generator.\n";

    return 0;
}