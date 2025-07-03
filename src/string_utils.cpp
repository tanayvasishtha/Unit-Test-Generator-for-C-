#include "string_utils.h"
#include <algorithm>
#include <cctype>
#include <sstream>
#include <regex>

std::string StringUtils::reverse(const std::string &str)
{
    std::string result = str;
    std::reverse(result.begin(), result.end());
    return result;
}

std::string StringUtils::toUpperCase(const std::string &str)
{
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::toupper);
    return result;
}

std::string StringUtils::toLowerCase(const std::string &str)
{
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), ::tolower);
    return result;
}

bool StringUtils::isPalindrome(const std::string &str)
{
    std::string cleaned;
    for (char c : str)
    {
        if (std::isalnum(c))
        {
            cleaned += std::tolower(c);
        }
    }
    return cleaned == reverse(cleaned);
}

int StringUtils::countVowels(const std::string &str)
{
    int count = 0;
    for (char c : str)
    {
        if (isVowel(std::tolower(c)))
        {
            count++;
        }
    }
    return count;
}

int StringUtils::countWords(const std::string &str)
{
    if (str.empty())
    {
        return 0;
    }

    std::istringstream iss(str);
    std::string word;
    int count = 0;

    while (iss >> word)
    {
        count++;
    }

    return count;
}

std::vector<std::string> StringUtils::split(const std::string &str, char delimiter)
{
    std::vector<std::string> result;
    std::istringstream stream(str);
    std::string token;

    while (std::getline(stream, token, delimiter))
    {
        result.push_back(token);
    }

    return result;
}

std::string StringUtils::join(const std::vector<std::string> &strings, const std::string &delimiter)
{
    if (strings.empty())
    {
        return "";
    }

    std::string result = strings[0];
    for (size_t i = 1; i < strings.size(); ++i)
    {
        result += delimiter + strings[i];
    }

    return result;
}

bool StringUtils::isValidEmail(const std::string &email)
{
    // Simple email validation using regex
    const std::regex pattern(R"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})");
    return std::regex_match(email, pattern);
}

bool StringUtils::isNumeric(const std::string &str)
{
    if (str.empty())
    {
        return false;
    }

    size_t start = 0;
    if (str[0] == '+' || str[0] == '-')
    {
        start = 1;
    }

    for (size_t i = start; i < str.length(); ++i)
    {
        if (!std::isdigit(str[i]))
        {
            return false;
        }
    }

    return true;
}

bool StringUtils::isVowel(char c)
{
    return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
}