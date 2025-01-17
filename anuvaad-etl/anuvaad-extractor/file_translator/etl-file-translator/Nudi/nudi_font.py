import re

def process_vattakshara(letters, t):
    """ Current char is t, which is ASCII code of vattakshara
    Rearrangement of string needed, If prev char is dependent vowel
    then it has to be moved after vattakshara
    If no dependent vowel then it is "ಅ" kaara, Ex: ಕ, ಗ
    Vattakshara shares same code as of base letter, but halant is added before
    Ex: ತಿಮ್ಮಿ in ASCII: ತಿ + ಮಿ + ma_vattu
    in Unicode: ತ + dependent vowel ಇ + ಮ + halant + ಮ + dependent vowel ಇ
    """
    
    # Default values
    last_letter = ""
    second_last = ""
    op = ""

    # If atleast one letter in letters, to find the last letter value
    if len(letters) > 0:
        last_letter = letters[-1]

    # If atleast two letters in letters, to find the second last letter value
    if len(letters) > 1:
        second_last = letters[-2]

    if last_letter in dependent_vowels:    
        # If last letter/prev letter to vattakshara is dependent vowel
        # add dependent vowel at the end, after halant + base letter(=vattakshara)
        letters[-1] = "್"
        letters.append(vattaksharagalu[t])
        letters.append(last_letter)
    else:
        # If "ಅ" kaara, just append halant + base letter
        # No worry about rearranging
        letters.append("್")
        letters.append(vattaksharagalu[t])

    # Return converted
    return letters


def process_arkavattu(letters, t):
    """ Example: ವರ್ಷ in ASCII ವ + ಷ + arkavattu
    in Unicode ವ + ರ + halant + ಷ
    """

    last_letter = ""
    second_last = ""

    # If atleast one letter in letters, to find the last letter value    
    if len(letters) > 0:
        last_letter = letters[-1]

    # If atleast two letters in letters, to find the second last letter value        
    if len(letters) > 1:
        second_last = letters[-2]

    # Rearrangement according to above example
    if last_letter in dependent_vowels:    
        letters[-2] = ascii_arkavattu[t]
        letters[-1] = "್"
        letters.append(second_last)
        letters.append(last_letter)
    else:
        letters[-1] = ascii_arkavattu[t]
        letters.append("್")
        letters.append(last_letter)

    # Return converted
    return letters


def process_broken_cases(letters, t):
    """ Since ASCII mapping are based on shapes some of the shapes
    give trouble with direct conversion
    Ex: ಕೀರ್ತಿ and ಕೇಳಿ In ASCII: deerga has same code in both but in
    Unicode both are different, So if prev char is "ಇ" kaara then
    behave differently and also with "ಎ" kaara
    Look at the prev char and also current char t and decide on the single unicode
    dependent vowel and substitute.
    Note prev char + current char = new char (Except ಉ kaara, ಕು = ಕ + ಉ kaara)
    since prev char is not dependent vowel
    """

    # Defaults
    last_letter = ""
    second_last = ""

    # If atleast one letter in letters, to find the last letter value    
    if len(letters) > 0:
        last_letter = letters[-1]    

    # Get dependent vowel mapping with respect to input "t"
    broken_case_mapping = broken_cases[t]["mapping"]

    if last_letter in broken_case_mapping:
        # If mapping exists
        letters[-1] = broken_case_mapping[last_letter]
    else :
        # For ಉ kaara, no mapping, substitute the value
        letters.append(broken_cases[t]["value"])

    # Return the converted
    return letters
   

def find_mapping(op, txt, current_pos):
    """ Finds mapping in reverse order, For Example if input string
    is abcde then itteration will be for abcde, abcd, abc, ab, a
    Only when mapping available the index jumps, say if mapping availabale for ab
    then subtract length of ab while processing next
    """    
    # Combination length, if length remaining is less than max len then
    # Consider length remaining as max length
    # remaining length = len(txt) - current_pos
    max_len = 4
    remaining = len(txt)-current_pos
    if remaining < 5:
        max_len = (remaining - 1)

    # Number of letters found mapping, will be returned to caller and
    # used to jump the index (Zero if one char found mapping)
    n = 0

   
    # Loop 4 to 0 or max to 0
    # Controller which checks direct mapping,
    # arkavattu, vattaksharagalu and broken cases
    for i in range(max_len,-1,-1):
        substr_till = current_pos + i + 1
        t = txt[current_pos:substr_till]

        if t in mapping:
            # If prev char is halant and current char is not vattakshara?
            # then it must be seperated using ZWJ, so that it will not
            # mix with prev char. 
            if len(op) > 0 and re.search("್$", op[-1]) != None:
                zwj =  "‍"
                op.append(zwj)
                
            # Direct mapping case
            op.append(mapping[t])

            # Update Jump by number
            n = i
            
            # Break and return to caller since we found the mapping
            # for given input
            break
        else:
            # Try without processing till reaches to last char 
            if i > 0:
                continue

            op = list(''.join(op)) #
            # If Last in this batch
            if t in ascii_arkavattu:
                # Arkavattu
                op = process_arkavattu(op, t)
            elif t in vattaksharagalu:
                # Vattakshara
                op = process_vattakshara(op, t)
            elif t in broken_cases:
                # Broken cases
                op = process_broken_cases(op, t)
            else:
                # No match
                op.append(t)
            
    return [n, op]
def process_line(line):
    """Splits the line into words and processes each word
    """
    print('lines-----',line)
    # Clean the input
    # line = line.strip() #----------------- changed

    # Into words
    words = line.split(' ')

    # To stote converted words
    op_words = []

    # Process and append to main array
    for word in words:
        op_words.append(process_word(word))
    print('done',op_words)
    # Return converted line
    return ' '.join(op_words)
def process_word(word):
    """Main program to process the word letter by letter
    """
    
    # Initiate and output Array
    i = 0
    max_len = len(word)
    op = []

    while i < max_len:
        # For each letter in word, jump if data[0] is more than zero

        # If additional chars used in ASCII to improve readability,
        # which doesn't have any significant in Unicode
        if word[i] in ignore_list:
            i += 1
            continue
#         print('word',word)
        # Find the mapping data
        data = find_mapping(op, word, i)
#         print('data-----------',data)
        # Add to final list
        op = data[1]

        # Jump if data[0]>0 which means found a match for more than
        # one letter combination
        i += (1 + data[0])

    # Return processed
    return ''.join(op)
    
def process_line(line):
    """Splits the line into words and processes each word
    """
#     print('lines-----',line)
    # Clean the input
    # line = line.strip() #----------------- changed

    # Into words
    words = line.split(' ')

    # To stote converted words
    op_words = []

    # Process and append to main array
    for word in words:
        op_words.append(process_word(word))
#     print('done',op_words)
    # Return converted line
    return ''.join(op_words)


mapping = {
    "C"     : "ಅ",
    "D"     : "ಆ",
    "E"     : "ಇ",
    "F"     : "ಈ",
    "G"     : "ಉ",
    "H"     : "ಊ",
    "IÄ"    : "ಋ",
    "J"     : "ಎ",
    "K"     : "ಏ",
    "L"     : "ಐ",
    "M"     : "ಒ",
    "N"     : "ಓ",
    "O"     : "ಔ",
    "A"     : "ಂ",
    "B"     : "ಃ",
    "Pï"    : "ಕ್",
    "PÀ"    : "ಕ",
    "PÁ"    : "ಕಾ", 
    "Q"     : "ಕಿ",
    "PÉ"    : "ಕೆ",
    "PË"    : "ಕೌ",
    "Sï"    : "ಖ್",
    "R"     : "ಖ",
    "SÁ"    : "ಖಾ",
    "T"     : "ಖಿ",
    "SÉ"    : "ಖೆ",
    "SË"    : "ಖೌ",
    "Uï"    : "ಗ್",
    "UÀ"    : "ಗ",
    "UÁ"    : "ಗಾ",
    "V"     : "ಗಿ",
    "UÉ"    : "ಗೆ",
    "UË"    : "ಗೌ",
    "Wï"    : "ಘ್",
    "WÀ"    : "ಘ",
    "WÁ"    : "ಘಾ",
    "X"     : "ಘಿ",
    "WÉ"    : "ಘೆ",
    "WË"    : "ಘೌ",
    "k"     : "ಞ",
    "Zï"    : "ಚ್",
    "ZÀ"    : "ಚ",
    "ZÁ"    : "ಚಾ",
    "a"     : "ಚಿ",
    "ZÉ"    : "ಚೆ",
    "ZË"    : "ಚೌ",
    "bï"    : "ಛ್",
    "bÀ"    : "ಛ",
    "bÁ"    : "ಛಾ",
    "c"     : "ಛಿ",
    "bÉ"    : "ಛೆ",
    "bË"    : "ಛೌ",
    "eï"    : "ಜ್",
    "d"     : "ಜ",
    "eÁ"    : "ಜಾ",
    "f"     : "ಜಿ",
    "eÉ"    : "ಜೆ",
    "eË"    : "ಜೌ",
    "gÀhiï" : "ಝ್",
    "gÀhÄ"  : "ಝ",
    "gÀhiÁ" : "ಝಾ",
    "jhÄ"   : "ಝಿ",
    "gÉhÄ"  : "ಝೆ",
    "gÉhÆ"  : "ಝೊ",
    "gÀhiË" : "ಝೌ",
    "Y"     : "ಙ",
    "mï"    : "ಟ್",
    "l"     : "ಟ",
    "mÁ"    : "ಟಾ",
    "n"     : "ಟಿ",
    "mÉ"    : "ಟೆ",
    "mË"    : "ಟೌ",
    "oï"    : "ಠ್",
    "oÀ"    : "ಠ",
    "oÁ"    : "ಠಾ",
    "p"     : "ಠಿ",
    "oÉ"    : "ಠೆ",
    "oË"    : "ಠೌ",
    "qï"    : "ಡ್",
    "qÀ"    : "ಡ",
    "qÁ"    : "ಡಾ",
    "r"     : "ಡಿ",
    "qÉ"    : "ಡೆ",
    "qË"    : "ಡೌ",
    "qsï"   : "ಢ್",
    "qsÀ"   : "ಢ",
    "qsÁ"   : "ಢಾ",
    "rü"    : "ಢಿ",
    "qsÉ"   : "ಢೆ",
    "qsË"   : "ಢೌ",
    "uï"    : "ಣ್",
    "t"     : "ಣ",
    "uÁ"    : "ಣಾ",
    "tÂ"    : "ಣಿ",
    "uÉ"    : "ಣೆ",
    "uË"    : "ಣೌ",
    "vï"    : "ತ್",
    "vÀ"    : "ತ",
    "vÁ"    : "ತಾ",
    "w"     : "ತಿ",
    "vÉ"    : "ತೆ",
    "vË"    : "ತೌ",
    "xï"    : "ಥ್",
    "xÀ"    : "ಥ",
    "xÁ"    : "ಥಾ",
    "y"     : "ಥಿ",
    "xÉ"    : "ಥೆ",
    "xË"    : "ಥೌ",
    "zï"    : "ದ್",
    "zÀ"    : "ದ",
    "zÁ"    : "ದಾ",
    "¢"     : "ದಿ",
    "zÉ"    : "ದೆ",
    "zË"    : "ದೌ",
    "zsï"   : "ಧ್",
    "zsÀ"   : "ಧ",
    "zsÁ"   : "ಧಾ",
    "¢ü"    : "ಧಿ",
    "zsÉ"   : "ಧೆ",
    "zsË"   : "ಧೌ",
    "£ï"    : "ನ್",
    "£À"    : "ನ",
    "£Á"    : "ನಾ",
    "¤"     : "ನಿ",
    "£É"    : "ನೆ",
    "£Ë"    : "ನೌ",
    "¥ï"    : "ಪ್",
    "¥À"    : "ಪ",
    "¥Á"    : "ಪಾ",
    "¦"     : "ಪಿ",
    "¥É"    : "ಪೆ",
    "¥Ë"    : "ಪೌ",
    "¥sï"   : "ಫ್",
    "¥sÀ"   : "ಫ",
    "¥sÁ"   : "ಫಾ",
    "¦ü"    : "ಫಿ",
    "¥sÉ"   : "ಫೆ",
    "¥sË"   : "ಫೌ",
    "¨ï"    : "ಬ್",
    "§"     : "ಬ",
    "¨Á"    : "ಬಾ",
    "©"     : "ಬಿ",
    "¨É"    : "ಬೆ",
    "¨Ë"    : "ಬೌ",
    "¨sï"   : "ಭ್",
    "¨sÀ"   : "ಭ",
    "¨sÁ"   : "ಭಾ",
    "©ü"    : "ಭಿ",
    "¨sÉ"   : "ಭೆ",
    "¨sË"   : "ಭೌ",
    "ªÀiï"  : "ಮ್",
    "ªÀÄ"   : "ಮ",
    "ªÀiÁ"  : "ಮಾ",
    "«Ä"    : "ಮಿ",
    "ªÉÄ"   : "ಮೆ",
    "ªÀiË"  : "ಮೌ",
    "AiÀiï" : "ಯ್",
    "AiÀÄ"  : "ಯ",
    "0iÀÄ"  : "ಯ",
    "AiÀiÁ" : "ಯಾ",
    "0iÀiÁ" : "ಯಾ",
    "¬Ä"    : "ಯಿ",
    "0iÀÄÄ" : "ಯು",
    "AiÉÄ"  : "ಯೆ",
    "0iÉÆ"  : "ಯೊ",
    "AiÉÆ"  : "ಯೊ",
    "AiÀiË" : "ಯೌ",
    "gï"    : "ರ್",
    "gÀ"    : "ರ",
    "gÁ"    : "ರಾ",
    "j"     : "ರಿ",
    "gÉ"    : "ರೆ",
    "gË"    : "ರೌ",
    "¯ï"    : "ಲ್",
    "®"     : "ಲ",
    "¯Á"    : "ಲಾ",
    "°"     : "ಲಿ",
    "¯É"    : "ಲೆ",
    "¯Ë"    : "ಲೌ",
    "ªï"    : "ವ್",
    "ªÀ"    : "ವ",
    "ªÁ"    : "ವಾ",
    "«"     : "ವಿ",
    "ªÀÅ"   :"ವು",
    "ªÀÇ"   :"ವೂ",
    "ªÉ"    :"ವೆ",
    "ªÉÃ"   :"ವೇ",
    "ªÉÊ"   :"ವೈ",
    "ªÉÆ"   :"ಮೊ",
    "ªÉÆÃ"  :"ಮೋ",
    "ªÉÇ"   :"ವೊ",
    "ªÉÇÃ"  :"ವೋ",
    "ªÉ  "  : "ವೆ",
    "¥ÀÅ"   : "ಪು",
    "¥ÀÇ"   : "ಪೂ",
    "¥sÀÅ"  : "ಫು", 
    "¥sÀÇ"  : "ಫೂ",
    "ªË"    : "ವೌ",
    "±ï"    : "ಶ್",
    "±À"    : "ಶ",
    "±Á"    : "ಶಾ",
    "²"     : "ಶಿ",
    "±É"    : "ಶೆ",
    "±Ë"    : "ಶೌ",
    "µï"    : "ಷ್",
    "µÀ"    : "ಷ",
    "µÁ"    : "ಷಾ",
    "¶"     : "ಷಿ",
    "µÉ"    : "ಷೆ",
    "µË"    : "ಷೌ",
    "¸ï"    : "ಸ್",
    "¸À"    : "ಸ",
    "¸Á"    : "ಸಾ",
    "¹"     : "ಸಿ",
    "¸É"    : "ಸೆ",
    "¸Ë"    : "ಸೌ",
    "ºï"    : "ಹ್",
    "ºÀ"    : "ಹ",
    "ºÁ"    : "ಹಾ",
    "»"     : "ಹಿ",
    "ºÉ"    : "ಹೆ",
    "ºË"    : "ಹೌ",
    "¼ï"    : "ಳ್",
    "¼À"    : "ಳ",
    "¼Á"    : "ಳಾ",
    "½"     : "ಳಿ",
    "¼É"    : "ಳೆ",
    "¼Ë"    : "ಳೌ"
    }

# These when joined will be broken as per unicode
broken_cases = {
    "Ã":{
        "value": "ೀ",
        "mapping": {
            "ಿ": "ೀ",
            "ೆ": "ೇ",
            "ೊ": "ೋ"
            }
        }, 
    "Ä":{
        "value": "ು",
        "mapping": {
            
            }
        }, 
    "Æ":{
        "value": "ೂ",
        "mapping": {
            "ೆ":"ೊ"
            }
        }, 
    "È":{
        "value": "ೃ",
        "mapping": {
            
            }
        }, 
    "Ê":{
        "value": "ೈ",
        "mapping": {
            "ೆ":"ೈ"
            }
        }  
    }

# Halant and dependent vowels
dependent_vowels = ["್", "ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ"]

# Spacing chars in ASCII, can be ignored while converting to Unicode
ignore_list = {"ö": "", "÷": ""}

# ASCII vattaksharagalu and Unicode replacements
vattaksharagalu = {
    "Ì" : "ಕ",
    "Í" : "ಖ",
    "Î" : "ಗ",
    "Ï" : "ಘ",
    "Õ" : "ಞ",
    "Ñ" : "ಚ",
    "Ò" : "ಛ",
    "Ó" : "ಜ",
    "Ô" : "ಝ",
    "Ö" : "ಟ",
    "×" : "ಠ",
    "Ø" : "ಡ",
    "Ù" : "ಢ",
    "Ú" : "ಣ",
    "Û" : "ತ",
    "Ü" : "ಥ",
    "Ý" : "ದ",
    "Þ" : "ಧ",
    "ß" : "ನ",
    "à" : "ಪ",
    "á" : "ಫ",
    "â" : "ಬ",
    "ã" : "ಭ",
    "ä" : "ಮ",
    "å" : "ಯ",
    "æ" : "ರ",
    "è" : "ಲ",
    "é" : "ವ",
    "ê" : "ಶ",
    "ë" : "ಷ",
    "ì" : "ಸ",
    "í" : "ಹ",
    "î" : "ಳ",
    "ç" : "ರ"
    }

# Arkavattu and Unicode replacement
ascii_arkavattu = {
    "ð": "ರ"
    }
