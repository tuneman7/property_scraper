#!/usr/bin/python

my_input = "bozo"
next_string = ''

m_len=len(my_input)
print(m_len)
while m_len > 0:
    print(m_len)
    next_string = next_string + my_input[m_len-1]
    m_len-=1

print(next_string)

s1 = ''
for c in my_input:
    s1 = c + s1  # appending chars in reverse order

print(s1)
s2=''
new_string = [s2 + c for c in my_input]

print(new_string)

input_good = True
try:
    input_word = input("Enter a word:")
    if not isinstance(input_word, str):
        print("You have entered zero letters so a vowel density cannot be computed.")
        input_good=False
    #    if len(input_word.strip()==0):
    #        print("You have entered zero letters so a vowel density cannot be computed.")
    #        input_good=False
    input_vowel = input("Enter a vowel:")
    if not isinstance(input_vowel, str):
        print("You have not entered a vowel letters so a vowel density cannot be computed.")
        input_good = False
    if len(input_vowel.strip() == 0):
        print("You have entered zero letters so a vowel density cannot be computed.")
        input_good = False
    if (input_good):
        print("fido")
        # number_of_letters = vowel_density(input_word, input_vowel)
        # print("{} of the letters in {} are \"{}\".".format(number_of_letters, input_word, input_vowel))
except:
    print("There was an error in the input provided.")
")

