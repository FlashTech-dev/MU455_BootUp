import re
import string
from emot.emo_unicode import UNICODE_EMO, EMOTICONS
import emot
import emojis
import csv
from statistics import mean
from googletrans import Translator
from textblob import TextBlob
from itertools import groupby
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

translator = Translator()

#########################################################################################################################################################################
#------------------------------------------------------------------------------------Emoji Analysis---------------------------------------------------------------------#
#########################################################################################################################################################################

def emojiRefinement(removePunctuation): 
    er = re.findall(r'[^\w\s+,]', removePunctuation)
    return er
    
def emojiToWordRefinement(er):
    etw = []
    for i in er: etw.append(emojiToWord(i).replace("_"," ").replace(":","").upper().strip())
    return etw
    
def emojiToWord(inputEmoji):
    inputEmojiCopy = inputEmoji
    for emot in UNICODE_EMO: inputEmoji = inputEmoji.replace(emot,(UNICODE_EMO[emot]))
    if(inputEmojiCopy == inputEmoji): inputEmoji = emojis.decode(inputEmoji)
    return str(inputEmoji)

def emojiAnalyser(inputString):
    inputString = re.sub(r'[१२३४५६७८९०अआइईउऊएऐओऔअंअःककाकिकीकुकूकेकैकोकौकंकःखखाखिखीखुखूखेखैखोखौखंखःगगागिगीगुगूगेगैगोगौगंगःघघाघिघीघुघूघेघैघोघौघंघःचचाचिचीचुचूचेचैचोचौचंचःछछाछिछीछुछूछेछैछोछौछंछःजजाजिजीजुजूजेजैजोजौजंजःझझाझिझीझुझूझेझैझोझौझंझःटटाटिटीटुटूटेटैटोटौटंटःठठाठिठीठुठूठेठैठोठौठंठःडडाडिडीडुडूडेडैडोडौडंडःढढाढिढीढुढूढेढैढोढौढंढःणणाणिणीणुणूणेणैणोणौणंणःततातितीतुतूतेतैतोतौतंतःथथाथिथीथुथूथेथैथोथौथंथःददादिदीदुदूदेदैदोदौदंदःधधाधिधीधुधूधेधैधोधौधंधःननानिनीनुनूनेनैनोनौनंनःपपापिपीपुपूपेपैपोपौपंपःफफाफिफीफुफूफेफैफोफौफंफःबबाबिबीबुबूबेबैबोबौबंबःभभाभिभीभुभूभेभैभोभौभंभःममामिमीमुमूमेमैमोमौमंमःययायियीयुयूयेयैयोयौयंयःररारिरीरुरूरेरैरोरौरंरःललालिलीलुलूलेलैलोलौलंलःळळाळिळीळुळूळेळैळोळौळंळःववाविवीवुवूवेवैवोवौवंवःशशाशिशीशुशूशेशैशोशौशंशःषषाषिषीषुषूषेषैषोषौषंषःससासिसीसुसूसेसैसोसौसंसःहहाहिहीहुहूहेहैहोहौहंहःक्षक्षाक्षिक्षीक्षुक्षूक्षेक्षैक्षोक्षौक्षंक्षःत्रत्रात्रित्रीत्रुत्रूत्रेत्रैत्रोत्रौत्रंत्रःज्ञज्ञाज्ञिज्ञीज्ञुज्ञूज्ञेज्ञैज्ञोज्ञौज्ञंज्ञःश्रश्राश्रिश्रीश्रुश्रूश्रेश्रैश्रोश्रौश्रंश्रः-ािीुूेैोौंःॐ]','',inputString)
    emojiInputString = inputString
    er = emojiRefinement(inputString) #return a list with only emoji's extracted from input sentence
    if(er != []):
        print("The emoji's extracted from input are : ",er)
        etw = emojiToWordRefinement(er) #returns a list with word form of the emojis
        print("The emoji's converted to words are : ",etw)
        return etw

def emoticonAnalyser(inputString):
    inputString = re.sub(r'[१२३४५६७८९०अआइईउऊएऐओऔअंअःककाकिकीकुकूकेकैकोकौकंकःखखाखिखीखुखूखेखैखोखौखंखःगगागिगीगुगूगेगैगोगौगंगःघघाघिघीघुघूघेघैघोघौघंघःचचाचिचीचुचूचेचैचोचौचंचःछछाछिछीछुछूछेछैछोछौछंछःजजाजिजीजुजूजेजैजोजौजंजःझझाझिझीझुझूझेझैझोझौझंझःटटाटिटीटुटूटेटैटोटौटंटःठठाठिठीठुठूठेठैठोठौठंठःडडाडिडीडुडूडेडैडोडौडंडःढढाढिढीढुढूढेढैढोढौढंढःणणाणिणीणुणूणेणैणोणौणंणःततातितीतुतूतेतैतोतौतंतःथथाथिथीथुथूथेथैथोथौथंथःददादिदीदुदूदेदैदोदौदंदःधधाधिधीधुधूधेधैधोधौधंधःननानिनीनुनूनेनैनोनौनंनःपपापिपीपुपूपेपैपोपौपंपःफफाफिफीफुफूफेफैफोफौफंफःबबाबिबीबुबूबेबैबोबौबंबःभभाभिभीभुभूभेभैभोभौभंभःममामिमीमुमूमेमैमोमौमंमःययायियीयुयूयेयैयोयौयंयःररारिरीरुरूरेरैरोरौरंरःललालिलीलुलूलेलैलोलौलंलःळळाळिळीळुळूळेळैळोळौळंळःववाविवीवुवूवेवैवोवौवंवःशशाशिशीशुशूशेशैशोशौशंशःषषाषिषीषुषूषेषैषोषौषंषःससासिसीसुसूसेसैसोसौसंसःहहाहिहीहुहूहेहैहोहौहंहःक्षक्षाक्षिक्षीक्षुक्षूक्षेक्षैक्षोक्षौक्षंक्षःत्रत्रात्रित्रीत्रुत्रूत्रेत्रैत्रोत्रौत्रंत्रःज्ञज्ञाज्ञिज्ञीज्ञुज्ञूज्ञेज्ञैज्ञोज्ञौज्ञंज्ञःश्रश्राश्रिश्रीश्रुश्रूश्रेश्रैश्रोश्रौश्रंश्रः-ािीुूेैोौंःॐ]','',inputString)
    #input = re.sub(r'^\s*[\(A-Za-z0-9\)]\s*','',inputString)
    input = re.sub(r'\(?[A-Za-z0-9]+\)',"",inputString)
    print('input is : ',input)
    wordEmoticon = []
    textEmoticons = re.split('\s',input)
    for emot in EMOTICONS:
    	input = re.sub(u'('+emot+')', "_".join(EMOTICONS[emot].replace(",","").split()), input)
    replaceEmoticons = re.split('\s',input)
    for i in range(len(replaceEmoticons)):
    	if(textEmoticons[i] != replaceEmoticons[i]):
    		wordEmoticon.append(replaceEmoticons[i].replace("_",' '))
    		
    return wordEmoticon
        
#########################################################################################################################################################################
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################################


######################################################################################################################################################################
#------------------------------------------------------------------------------------Text Analysis----------------------------------------------------------------------#
#########################################################################################################################################################################

def textAnalyser(removePunctuation):
    emojiAverageSentimentScore = emojiAnalyser(removePunctuation)
    removeEmoji = removeEmojis(removePunctuation)#Removes Emojis from sentence    
    print('Reduced Emojis is : ',removeEmoji)
    removeRepetitiveCharacters = removeRepetition(removeEmoji)
    print('The reduced repetition is : ',removeRepetitiveCharacters)
    langCheck,confidenceCheck = checkLanguage(removeRepetitiveCharacters)
    removeRepetitiveCharacters = removeRepetitiveCharacters +" "
    refinedEnglishStatement = (GoogleTranslate(langCheck,confidenceCheck,removeRepetitiveCharacters))
    print('The Refined statement is : ',refinedEnglishStatement )
    return refinedEnglishStatement 
#       langCheck , confidenceCheck = checkLanguage(removeRepetitiveCharacters)
        #clubingSentences = languageRefinement(removeRepetitiveCharacters)
        #

#----------------------------------------Reducing the repetition to 2-------------
                
             
def removeRepetition(s):
    return (re.sub( re.compile(r"([A-Za-z])\1{1,}", re.IGNORECASE),rpt_repl, s))

def rpt_repl(match):
  return match.group(1)+match.group(1)

def checkLanguage(removeRepetitiveCharacters):
    return str(getattr(translator.detect(removeRepetitiveCharacters),'lang')), float(translator.detect(removeRepetitiveCharacters).confidence) 

def GoogleTranslate(langCheck,confidenceCheck,removeRepetitiveCharacters):
    statementTranslation = ''
    try:
    	if(langCheck=='en' and confidenceCheck >=0.85):
                	statementTranslation = TextBlob(translator.translate(removeRepetitiveCharacters,dest = 'hi').text).translate(to = 'en')
                	print('English translation : ',statementTranslation)

    	elif(langCheck=='hi' and confidenceCheck >=0.85):
                	statementTranslation = TextBlob(translator.translate(removeRepetitiveCharacters,dest = 'hi').text).translate(to = 'en')
                	print('Hindi translation : ',statementTranslation)

    	else:
    		statementTranslation = refineTranslation(removeRepetitiveCharacters)
    		print('Enhanced Refined translation : ',statementTranslation)
    except:
    		statementTranslation = refineTranslation(removeRepetitiveCharacters)
    		print('Enhanced Refined translation : ',statementTranslation)
    		
    return str(statementTranslation)


def refineTranslation(removeRepetitiveCharacters):
	Googletranslated = translator.translate(removeRepetitiveCharacters).text
	if Googletranslated ==removeRepetitiveCharacters:
		statementTranslation = TextBlob(transliterate(removeRepetitiveCharacters, sanscript.ITRANS, sanscript.DEVANAGARI)).translate(to = 'en')
		#print('Refined translation : ',statementTranslation)
	else:
		statementTranslation = Googletranslated
		#print('Refined translation : ',Googletranslated)
	return statementTranslation

#---------------------------------------------------------------------------

def removePunctuationMarks(inputString):
    removePunctuation = (re.sub(r'''(?i)\b((?:ftp|https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", inputString))#Removes Websute names
    removePunctuation = re.sub(r"\S+@\S+[.]\S+","",removePunctuation)#Removes email address
    removePunctuation = re.sub(r"[.,?'\";:!~`^\\]", "",removePunctuation)#Removes Punctuation Marks
    removePunctuation = re.sub('\s*\(\S*|\s*\)\S*|\s*\{\S*|\s*\}\S*|\s*\[\S*|\s*\]\S*|\s*\S*\+\S*\s*|\s*\S*\-\S*\s*|\s*\S*\*\S*\s*|\s*\S*\/\S*\s*|\s*\S*\%\S*\s*|\s*\S*\>\S*\s*|\s*\S*\<\S*\s*|\s*\S\=+\S*\s*',' ',removePunctuation)#Removes all expressions
    removePunctuation = re.sub(r'_',' ',removePunctuation)#Replaces underscore by space
    removePunctuation = re.sub('[/$]',' Dollars ',removePunctuation)#Replaces $ by Dollars
    removePunctuation = re.sub(r'[/&]',' and ',removePunctuation)#Replaces & by and
    removePunctuation = re.sub(r'[/|]',' or ',removePunctuation)#Replaces | by or
    removePunctuation = re.sub(r'\s*@\S*|\s*#|\s*\d'," ",removePunctuation)#Removes @UserId and #Userid or #Comment and all Digits
    removePunctuation = re.sub(r'\s+',' ',removePunctuation)#Removes multiple spaces to single space
    return removePunctuation

#Note:website classified ->email-id->punctuations->expressions->underscore,Dollars,and,or->removing emojis->replacing multiple spaces by one

def removeEmojis(removePunctuation):
    temp = (re.findall(r'[^ा ि ी ु ू े ै ो ौ ं ः\w\s+,]', removePunctuation))#Removes Emojis and stores in a temporary variable
    for i in temp:
        removePunctuation = re.sub(i,'',removePunctuation)#Removes the Emojis using temporary variable   
    removePunctuation = re.sub(r'\s+',' ',removePunctuation)#Removes multiple spaces to single space
    return removePunctuation


#########################################################################################################################################################################
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################################


#########################################################################################################################################################################
#------------------------------------------------------------------------------------Main Function----------------------------------------------------------------------#
#########################################################################################################################################################################

def translate_text(inputString):
    removePunctuation = removePunctuationMarks(inputString).lower()#Removes website, email-id, punctuations, expressions, underscore, Dollars, and, or,replacing multiple spaces by one, and converts into lower case 
    print('Reduced punctuatons is : ',removePunctuation)
    emojiToWordList = emojiAnalyser(removePunctuation)
    emoticonAverageSentimentScore = emoticonAnalyser(inputString)
    print('The Average Emoticon Score is : ',emoticonAverageSentimentScore)
    refinedStatement = textAnalyser(removePunctuation) +  ' '
    if emojiToWordList !=None:
    	for i in emojiToWordList:
    		refinedStatement = refinedStatement + str(i) + ' '
    if emoticonAverageSentimentScore != []:
    	for i in emoticonAverageSentimentScore:
    		refinedStatement = refinedStatement + str(i).upper() + ' '		
    refinedStatement = refinedStatement.strip()		 		
    return refinedStatement
        
    # paraSplit = re.split(r'[.]',inputString);
    # print('the para list is : ',paraSplit)
    # paraCombine = ''
    # for i in paraSplit:
    #     removePunctuation = removePunctuationMarks(i.strip()).lower()#Removes website, email-id, punctuations, expressions, underscore, Dollars, and, or,replacing multiple spaces by one, and converts into lower case 
    #     print('Reduced punctuatons is : ',removePunctuation)
    #     emojiToWordList = emojiAnalyser(removePunctuation)
    #     emoticonAverageSentimentScore = emoticonAnalyser(i.strip())
    #     print('The Average Emoticon Score is : ',emoticonAverageSentimentScore)
    #     refinedStatement = textAnalyser(removePunctuation) +  ' '
    #     if emojiToWordList !=None:
    #         for i in emojiToWordList:
    #             refinedStatement = refinedStatement + str(i) + ' '
    #     if emoticonAverageSentimentScore != []:
    #         for i in emoticonAverageSentimentScore:
    #             refinedStatement = refinedStatement + str(i).upper() + ' '		
    #     refinedStatement = refinedStatement.strip()		 		
    #     print('The Emot converted Refined statement is : ',refinedStatement)
    #     paraCombine = paraCombine + refinedStatement + " "
    # print('The combined paragraph is : ',paraCombine.strip())

    # return paraCombine.strip()


#########################################################################################################################################################################
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#########################################################################################################################################################################