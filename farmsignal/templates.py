# AI-authored / source-checked draft. Native Urdu and agronomist review remain required.
T={
'forecast':('Check field moisture before sowing.','بوائی سے پہلے کھیت کی نمی دیکھیں۔'),
'clarify':('Please ask about growing maize, soil, weather, or speaking to an adviser.','براہ کرم مکئی کی کاشت، مٹی، موسم یا زرعی مشیر سے بات کرنے کے بارے میں پوچھیں۔'),
'location':('Please register your farm location before I check local conditions.','مقامی حالات جانچنے سے پہلے اپنے کھیت کا مقام درج کروائیں۔'),
'outside':('Your farm is outside my saved area. Ask a local agricultural adviser to check it.','آپ کا کھیت میرے محفوظ علاقے سے باہر ہے۔ مقامی زرعی مشیر سے اسے جانچنے کو کہیں۔'),
'crop':('Which crop do you want to grow? This demo can check maize only.','آپ کون سی فصل اگانا چاہتے ہیں؟ یہ نمونہ صرف مکئی کی جانچ کر سکتا ہے۔'),
'unsupported':('This demo checks maize only. Ask a local adviser about your crop.','یہ نمونہ صرف مکئی کی جانچ کرتا ہے۔ اپنی فصل کے بارے میں مقامی مشیر سے پوچھیں۔'),
'referral':('Referral simulated. No officer has been contacted. Please contact your local extension office.','یہ رابطہ صرف نمونہ ہے۔ کسی افسر سے رابطہ نہیں ہوا۔ اپنے مقامی زرعی دفتر سے رابطہ کریں۔'),
'referral_failed':('The simulated referral failed. No officer was contacted. Please contact your local extension office.','نمائشی رابطہ ناکام ہوا۔ کسی افسر سے رابطہ نہیں ہوا۔ مقامی زرعی دفتر سے رابطہ کریں۔'),
'drainage':('You reported standing water. Ask a local adviser to check drainage before planting maize.','آپ نے کھڑے پانی کی اطلاع دی ہے۔ مکئی لگانے سے پہلے مقامی مشیر سے پانی کی نکاسی جانچنے کو کہیں۔'),
'dry':('You reported dry soil. Check moisture below the surface before sowing maize.','آپ نے خشک مٹی کی اطلاع دی ہے۔ مکئی بونے سے پہلے سطح کے نیچے نمی دیکھیں۔'),
'ph':('The soil map suggests a possible acidity limitation. Have your field soil tested before deciding on maize.','مٹی کے نقشے میں تیزابیت کی ممکنہ رکاوٹ ہے۔ مکئی کا فیصلہ کرنے سے پہلے کھیت کی مٹی کا ٹیسٹ کروائیں۔'),
'soil_missing':('I do not have reliable soil values for this field. Have the soil tested before deciding on maize.','اس کھیت کی مٹی کے معتبر اعداد موجود نہیں۔ مکئی کا فیصلہ کرنے سے پہلے مٹی کا ٹیسٹ کروائیں۔'),
'weather':('I have no usable current forecast. Check a fresh local forecast before choosing a sowing day.','موسم کی قابل استعمال تازہ پیش گوئی موجود نہیں۔ بوائی کا دن چننے سے پہلے مقامی تازہ پیش گوئی دیکھیں۔'),
'drainage_question':('The soil map cannot confirm suitability. Does water remain in your field after rain?','مٹی کا نقشہ موزونیت کی تصدیق نہیں کر سکتا۔ کیا بارش کے بعد کھیت میں پانی رہتا ہے؟'),
'moisture':('Check moisture below the soil surface before sowing. These records cannot confirm that maize will grow well.','بوائی سے پہلے مٹی کی سطح کے نیچے نمی دیکھیں۔ ان اعداد سے مکئی کی اچھی پیداوار کی تصدیق نہیں ہو سکتی۔')}
def render(key,language):return T[key][1 if language=='ur' else 0]
LANGUAGES={'en':{'enabled':True,'reviewed':False},'ur':{'enabled':True,'reviewed':False,'purpose':'Multilingual demonstration, not primary pilot language'},'sw':{'enabled':False,'reviewed':False}}
