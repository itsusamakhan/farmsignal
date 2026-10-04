"""AI-authored prototype questions, never represented as farmer observations."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# Each bilingual pair is a semantic family, kept entirely in one split.
DATA={
'planting':[
('Can I grow maize here?','کیا میں یہاں مکئی اُگا سکتا ہوں؟'),('Is this farm suitable for corn?','کیا یہ کھیت مکئی کے لیے موزوں ہے؟'),('I want to plant maize on my land','میں اپنی زمین پر مکئی لگانا چاہتا ہوں'),('Can maize grow in my field?','کیا میرے کھیت میں مکئی اگ سکتی ہے؟'),('Should I sow corn here?','کیا میں یہاں مکئی بوؤں؟'),('Check this land for planting maize','مکئی لگانے کے لیے اس زمین کو دیکھیں'),('Will my farm support maize?','کیا میرے کھیت میں مکئی ہو سکتی ہے؟'),('I plan to cultivate maize','میں مکئی کاشت کرنے کا ارادہ رکھتا ہوں'),
('Would corn do well on this plot?','کیا اس قطعے پر مکئی اچھی ہو گی؟'),('Thinking of starting a maize crop','مکئی کی فصل شروع کرنے کا سوچ رہا ہوں'),
('Before buying maize seed what should I check?','مکئی کا بیج خریدنے سے پہلے کیا دیکھوں؟'),('Is growing corn possible at my registered farm?','کیا میرے درج شدہ کھیت پر مکئی کی کاشت ممکن ہے؟'),('Considering maize for my next season','اگلے موسم میں مکئی کی کاشت پر غور کر رہا ہوں'),('Tell me the limitations for maize cultivation','مکئی کی کاشت کی رکاوٹیں بتائیں')],
'soil':[
('My soil is acidic','میری مٹی تیزابی ہے'),('What is the soil pH?','مٹی کا پی ایچ کیا ہے؟'),('The field is waterlogged','کھیت میں پانی کھڑا ہے'),('Is my soil too sandy?','کیا میری مٹی بہت ریتلی ہے؟'),('I need a soil test','مجھے مٹی کا ٹیسٹ چاہیے'),('Check the clay in my soil','میری مٹی میں چکنی مٹی دیکھیں'),('The soil is hard and dry','مٹی سخت اور خشک ہے'),('How is the soil quality here?','یہاں مٹی کی کیفیت کیسی ہے؟'),
('Water stays on my land after rain','بارش کے بعد میری زمین پر پانی رہتا ہے'),('Could soil acidity affect my crop?','کیا مٹی کی تیزابیت فصل پر اثر ڈال سکتی ہے؟'),
('There are puddles in the maize field','مکئی کے کھیت میں پانی کے گڑھے ہیں'),('Where can I check the acidity of this earth?','اس مٹی کی تیزابیت کہاں جانچ سکتا ہوں؟'),('The ground feels like heavy clay','زمین بھاری چکنی مٹی جیسی لگتی ہے'),('I worry about poor drainage','مجھے پانی کی ناقص نکاسی کی فکر ہے')],
'weather':[
('Will it rain tomorrow?','کیا کل بارش ہو گی؟'),('What is the weather forecast?','موسم کی پیش گوئی کیا ہے؟'),('How hot will it be?','کتنی گرمی ہو گی؟'),('Is rain expected this week?','کیا اس ہفتے بارش متوقع ہے؟'),('Tell me about rainfall here','یہاں کی بارش کے بارے میں بتائیں'),('What is the temperature?','درجہ حرارت کیا ہے؟'),('When will the rains come?','بارشیں کب آئیں گی؟'),('Do we have a fresh forecast?','کیا موسم کی تازہ پیش گوئی ہے؟'),
('Any chance of showers today?','کیا آج بارش کا امکان ہے؟'),('Has the coming weather been updated?','کیا آنے والے موسم کی خبر تازہ ہے؟'),
('Should I expect a dry spell next week?','کیا اگلے ہفتے خشک موسم کی توقع کروں؟'),('How much precipitation fell last season?','پچھلے موسم میں کتنی بارش ہوئی؟'),('Are temperatures rising over the weekend?','کیا ہفتے کے آخر میں درجہ حرارت بڑھ رہا ہے؟'),('Can you check the next few days of rain?','کیا اگلے چند دنوں کی بارش دیکھ سکتے ہیں؟')],
'officer':[
('I need an agricultural officer','مجھے زرعی افسر چاہیے'),('Please connect me to a human','مجھے کسی انسان سے رابطہ کروائیں'),('Can I speak to an adviser?','کیا میں مشیر سے بات کر سکتا ہوں؟'),('Refer me to an extension worker','مجھے زرعی کارکن کے پاس بھیجیں'),('I want expert help','مجھے ماہر کی مدد چاہیے'),('Contact an officer for me','میرے لیے افسر سے رابطہ کریں'),('I need a person to help','مجھے مدد کے لیے کسی شخص کی ضرورت ہے'),('Please arrange human support','براہ کرم انسانی مدد کا انتظام کریں'),
('Could an agronomist visit?','کیا زرعی ماہر آ سکتا ہے؟'),('Put me in touch with the extension service','مجھے زرعی توسیعی خدمت سے ملائیں'),
('I would rather discuss this with a real person','میں یہ کسی حقیقی شخص سے بات کرنا چاہوں گا'),('Who can advise me face to face?','کون مجھے سامنے بیٹھ کر مشورہ دے سکتا ہے؟'),('Find someone qualified to look at my farm','میرا کھیت دیکھنے کے لیے اہل شخص تلاش کریں'),('Could you pass my concern to a specialist?','کیا میری مشکل کسی ماہر تک پہنچا سکتے ہیں؟')],
'unknown':[
('Hello','سلام'),('What is the price of a tractor?','ٹریکٹر کی قیمت کیا ہے؟'),('Diagnose my sick cow','میری بیمار گائے کی بیماری بتائیں'),('Which pesticide should I spray?','کون سی کیڑے مار دوا چھڑکوں؟'),('How much fertilizer should I use?','کتنی کھاد استعمال کروں؟'),('Tell me a joke','مجھے لطیفہ سنائیں'),('My leaves have a disease','میرے پتوں کو بیماری ہے'),('Send me money','مجھے پیسے بھیجیں'),
('Book a bus ticket','بس کا ٹکٹ بک کریں'),('Something is wrong help','کچھ غلط ہے مدد کریں'),
('What is two plus two?','دو اور دو کتنے ہوتے ہیں؟'),('The goats refuse to eat','بکریاں کھانا نہیں کھا رہیں'),('How do I repair my phone?','میں اپنا فون کیسے ٹھیک کروں؟'),('Thanks goodbye','شکریہ خدا حافظ')]
}
rows=[]
for intent,pairs in DATA.items():
 for i,pair in enumerate(pairs):
  split='train' if i<8 else 'validation' if i<10 else 'test'
  for lang,text in zip(('en','ur'),pair):rows.append(dict(text=text,intent=intent,language=lang,family=f'{intent}-{i}',split=split,provenance='AI-authored synthetic; Urdu pair is AI translation; no human review'))
(ROOT/'data/intents.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(len(rows),'examples')
