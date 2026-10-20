import requests

url = "https://www.pricebefore.com/skullcandy-crusher-evo-40mm-drivers-40hr-p918702.html"

response = requests.get(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"

    },
    timeout=20,
)

response.raise_for_status()

html = response.text 

print("HTML length:", len(html))
print("Contains expected price:", "12999" in html)
print("First 2000 characters of HTML:")
print(html[:2000])