#pragma once
#include <string>
#include <vector>

class StringUtils
{
public:
    // String manipulation functions
    static std::string reverse(const std::string &str);
    static std::string toUpperCase(const std::string &str);
    static std::string toLowerCase(const std::string &str);

    // String analysis functions
    static bool isPalindrome(const std::string &str);
    static int countVowels(const std::string &str);
    static int countWords(const std::string &str);

    // String splitting and joining
    static std::vector<std::string> split(const std::string &str, char delimiter);
    static std::string join(const std::vector<std::string> &strings, const std::string &delimiter);

    // String validation
    static bool isValidEmail(const std::string &email);
    static bool isNumeric(const std::string &str);

private:
    static bool isVowel(char c);
};