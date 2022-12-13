import requests
import json

receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint

imageFile = "[IMAGE FILE HERE]" # path to image file

# access API and get receipt results as JSON file
receiptData = requests.post(receiptOcrEndpoint, data = {
  'api_key': '', # Use 'TEST' for testing purpose 
  'recognizer': 'US',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' 
  'ref_no': 'ocr_python_123', # optional caller provided ref code 
  }, 
  files = {"file": open(imageFile, "rb")})

# returns JSON object as a dictionary
receiptDic = json.loads(receiptData.text, strict=False)
  
# iterate through receipt and print: store name, store address, products, prices
for receipt in receiptDic['receipts']:
	print(receipt['merchant_name'])
	print(receipt['merchant_address'])
	for item in receipt['items']:
		print(item['description'])
		print(item['amount'])
  
# Closing file
receiptResults.close()
