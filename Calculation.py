import wolframalpha  #pip istall wolframalpha

app_id = 'GY69UP-43HL5Y5367'
client = wolframalpha.Client(app_id)

def calculation(text):
    value = client.query(text)
    result = next(value.results).text

    return result


