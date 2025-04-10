from openai import OpenAI

# Point to the local server
# client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
# client = OpenAI(api_key="sk-1234")  # unsafe to hardcode the API key
client = OpenAI()  # this assumes you have set the OPENAI_API_KEY environment variable

otsikko = "Mestarikirjoittaja"
print(otsikko)
print(len(otsikko) * "-")

while True:
    
    print("")

    print("Kirjoita syötteeseen millaisen tekstin haluat minun luovan tai lopeta kirjoittamalla q ja paina enter.")
    print("")
    content = input("syöte: ")
    if content == "q" or content == "Q":
        print("Ohjelma lopetettu")
        break
    else:
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Olet mestarikirjoittaja, joka tuottaa luovasti esimerkiksi markkinointimateriaaleja, meemejä, laulujen sanoituksia, runoja tai blogikirjoituksia. Sisältösi on hakukoneoptimoitu (SEO) käyttämällä mahdollisimman monia synonyymejä."},
                {"role": "user", "content": content}
            ],
                temperature=0.1,           
                top_p=0.95,                 
                presence_penalty=0.8,      
                frequency_penalty=0.4       
            )
    
        print("\n\ntemperature 0.1:\n" + response.choices[0].message.content)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Olet mestarikirjoittaja, joka tuottaa luovasti esimerkiksi markkinointimateriaaleja, meemejä, laulujen sanoituksia, runoja tai blogikirjoituksia. Sisältösi on hakukoneoptimoitu (SEO) käyttämällä mahdollisimman monia synonyymejä."},
                {"role": "user", "content": content}
            ],
                temperature=0.5,           
                top_p=0.95,                 
                presence_penalty=0.8,      
                frequency_penalty=0.4       
        )
    
        print("\n\ntemperature 0.5:\n" + response.choices[0].message.content)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Olet mestarikirjoittaja, joka tuottaa luovasti esimerkiksi markkinointimateriaaleja, meemejä, laulujen sanoituksia, runoja tai blogikirjoituksia. Sisältösi on hakukoneoptimoitu (SEO) käyttämällä mahdollisimman monia synonyymejä."},
                {"role": "user", "content": content}
            ],
                temperature=1.0,           
                top_p=0.95,                 
                presence_penalty=0.8,      
                frequency_penalty=0.4       
                
        )

        print("\n\ntemperature 1.0:\n" + response.choices[0].message.content)
