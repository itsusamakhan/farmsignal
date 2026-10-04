# AI-authored / source-checked draft. Native Urdu and agronomist review remain required.
T={
'forecast_horizon':('My saved forecast does not cover the full day you asked about. Check a fresh local forecast before deciding when to sow.','محفوظ پیش گوئی آپ کے پوچھے گئے پورے دن کا احاطہ نہیں کرتی۔ بوائی کا فیصلہ کرنے سے پہلے مقامی تازہ پیش گوئی دیکھیں۔'),
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
'ph':('The mapped soil range needs checking in your field. Have the soil tested before deciding on maize.','مٹی کے نقشے کے اندازے کی کھیت میں جانچ ضروری ہے۔ مکئی کا فیصلہ کرنے سے پہلے مٹی کا ٹیسٹ کروائیں۔'),
'verdict_feasible':('Maize: feasible here. Soil map (SoilGrids) shows pH {ph}. FAO EcoCrop: maize grows best at pH {lo}-{hi}. Next: confirm with a soil test before buying soil inputs.','مکئی: یہاں کاشت ممکن ہے۔ مٹی کا نقشہ (SoilGrids) pH {ph} دکھاتا ہے۔ FAO کے مطابق مکئی pH {lo} سے {hi} میں بہتر اگتی ہے۔ اگلا قدم: کچھ خریدنے سے پہلے مٹی کا ٹیسٹ کروائیں۔'),
'verdict_possible':('Maize: possible here. Soil map (SoilGrids) shows pH {ph}. FAO EcoCrop: maize grows best at pH {lo}-{hi} and tolerates {amin}-{amax}. Next: test your soil and ask an adviser before buying soil inputs.','مکئی: یہاں کاشت ہو سکتی ہے۔ مٹی کا نقشہ (SoilGrids) pH {ph} دکھاتا ہے۔ FAO کے مطابق مکئی pH {lo} سے {hi} میں بہتر اگتی ہے اور {amin} سے {amax} تک برداشت کرتی ہے۔ اگلا قدم: مٹی کا ٹیسٹ کروائیں اور کچھ خریدنے سے پہلے زرعی مشیر سے پوچھیں۔'),
'verdict_not_recommended':('Maize: not recommended here without advice. Soil map (SoilGrids) shows pH {ph}. FAO EcoCrop: maize tolerates pH {amin}-{amax}. Next: test your soil and ask an adviser before planting.','مکئی: مشورے کے بغیر یہاں کاشت کی سفارش نہیں۔ مٹی کا نقشہ (SoilGrids) pH {ph} دکھاتا ہے۔ FAO کے مطابق مکئی pH {amin} سے {amax} تک برداشت کرتی ہے۔ اگلا قدم: مٹی کا ٹیسٹ کروائیں اور بوائی سے پہلے زرعی مشیر سے پوچھیں۔'),
'soil_missing':('I do not have reliable soil values for this field. Have the soil tested before deciding on maize.','اس کھیت کی مٹی کے معتبر اعداد موجود نہیں۔ مکئی کا فیصلہ کرنے سے پہلے مٹی کا ٹیسٹ کروائیں۔'),
'weather':('I have no usable current forecast. Check a fresh local forecast before choosing a sowing day.','موسم کی قابل استعمال تازہ پیش گوئی موجود نہیں۔ بوائی کا دن چننے سے پہلے مقامی تازہ پیش گوئی دیکھیں۔'),
'drainage_question':('The soil map cannot confirm suitability. Does water remain in your field after rain?','مٹی کا نقشہ موزونیت کی تصدیق نہیں کر سکتا۔ کیا بارش کے بعد کھیت میں پانی رہتا ہے؟'),
'moisture':('Check moisture below the soil surface before sowing. These records cannot confirm that maize will grow well.','بوائی سے پہلے مٹی کی سطح کے نیچے نمی دیکھیں۔ ان اعداد سے مکئی کی اچھی پیداوار کی تصدیق نہیں ہو سکتی۔')}
def render(key,language,**values):
 text=T[key][1 if language=='ur' else 0]
 return text.format(**values) if values else text
LANGUAGES={'en':{'enabled':True,'reviewed':False},'ur':{'enabled':True,'reviewed':False,'purpose':'Multilingual demonstration, not primary pilot language'},'sw':{'enabled':False,'reviewed':False}}
