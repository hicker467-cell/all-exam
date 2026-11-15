from screenshot import capture_screenshot

path = capture_screenshot('https://scert.bihar.gov.in/examination-result/nmmss', 'scert_ssl_fix')
print("SSL Fix Result:", path)
