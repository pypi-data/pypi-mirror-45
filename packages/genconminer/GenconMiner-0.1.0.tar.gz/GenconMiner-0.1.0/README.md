# Gencon Miner

A general content miner that leverages on Beautiful Soup and Requests to handle extraction. The main goal is to always imagine in terms of targetting parent elements in an HTML form then getting group of tags given that parent.

```python
from gencon_miner import GenconMiner
```

## From URL

```python
url_miner = GenconMiner(url="http://google.com")
txt = url_miner.extract('title')
print(txt[0].text) # Google
```

## From text

```python
text_miner = GenconMiner(text="<p class='myclass'>Hello</p>")
txt = text_miner.extract('.myclass')
print(txt[0].text) # Hello
```

## Convert all tag content to string

Note that contents in a tag will be delimited using newline.

```python
meaning_of_life = """
    <p class='myclass'>
        Hello
        <span>darkness my old friend</span>
    </p>
    <b>And another one</b>
"""
bulk_miner = GenconMiner(text=meaning_of_life)
bulk_miner.to_text() # Hello\ndarkness my old friend\nAnd another one
```

## Author

Almer Mendoza
