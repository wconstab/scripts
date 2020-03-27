import pytest
import pathlib
import os
from ..wf_bot import interpret_content, load_html_file

asset_path = os.path.join(pathlib.Path(__file__).parent.absolute(), 'assets')

no_slots_available = ['no_slots_available-20200326-064732.html']
def test_no_slots_available():
    html_file = os.path.join(asset_path, no_slots_available[0])
    content = load_html_file(html_file)
    retry, message = interpret_content(content)
    assert retry == True
    assert message == "No slots available."

out_of_stock = [('out-of-stock-20200325-164602.html', 
                 ['Mango Yellow Conventional, 1 Each', 
                  'Pepper Thai Conventional, 0.25 lb']),
                ('out-of-stock-1-20200326-101550.html',
                 ['Chicken Thigh Air Chilled Non-Gmo Step 3']), 
                ('out-of-stock-4-20200326-130320.html',
                 ['Chicken Thigh Bone-In Air Chilled Organic Tray Pack Step 3', 
                  '365 Everyday Value, Toasted Sesame Seed Oil, 8.4 fl oz', 
                  'Apple Gala Organic, 1 Each', 'Banana Organic Whole Trade Guarantee, 1 Each', 
                  'Carrot Loose Organic, 0.5lb', 'Clover Sonoma Whole Milk, 32 Oz', 
                  'Clover Sonoma, Milk Reduced Fat Qt Organic, 32 Fluid', 
                  'Herb Cilantro Organic, 1 Bunch', 'Lemon Reg Conventional, 1 Each', 
                  'Lime Regular Conventional, 1 Each', 
                  'Lundberg Family Farms, California White Jasmine Rice, 32 Ounce (Pack of 1)', 
                  'Mandarin Clementine Conventional, 48 Ounce', 'Mango Yellow Conventional, 1 Each', 
                  'Mushroom Cremini Brown Organic, 0.5lb', 'Onion Green Scallion Conventional, 1 Bunch', 
                  'Organic Ginger Root', 'Pepper Fresno Conventional, 0.25 Lb', 
                  'Pineapple Whole Trade Gaurantee Organic, 1 Each', 'Pork Stew Meat Organic Step 3', 
                  'Raspberry Red Organic, 6 Ounce', 'Ritual Roasters, Coffee Seasonal, 12 Ounce', 
                  'Wildwood, Organic Sproutofu Extra Firm, 15.5 oz']),
                ]
@pytest.mark.parametrize("asset", out_of_stock)
def test_out_of_stock(asset):

    html_file = os.path.join(asset_path, asset[0])
    content = load_html_file(html_file)
    retry, message = interpret_content(content)
    assert retry == False
    items = asset[1]
    assert message == "{} items out of stock: {}".format(len(items), items)
