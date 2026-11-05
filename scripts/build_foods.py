#!/usr/bin/env python3
"""Ageligil food library v1: 1,000 dishes and drinks sold in Ethiopia, in 40 grids of 25 for image generation.

Run: python3 build_foods.py  ->  foods.json, prompts/grid-01.md .. grid-40.md, prompts/ALL.md
Ethiopian names and Amharic spellings need a native speaker's check (name_am is null where not confident).
Visual descriptions are written for an image model: what is on the plate, its colour, texture and serving.
"""
import json, os, re

# (name, amharic or None, category, tags, visual description)
ETH = []
def add(cat, rows):
    for r in rows:
        name, am, tags, desc = r
        ETH.append((name, am, cat, tags, desc))

add('stews (wot)', [
 ('Doro Wot', 'ዶሮ ወጥ', ['spicy'], 'deep red berbere chicken stew with a drumstick and a whole peeled boiled egg, glossy niter kibbeh sheen, on injera'),
 ('Doro Alicha', 'ዶሮ አልጫ', [], 'mild golden turmeric chicken stew with a boiled egg, served on injera'),
 ('Key Wot', 'ቀይ ወጥ', ['spicy'], 'dark red spicy beef stew in thick berbere sauce, on injera'),
 ('Siga Alicha', 'የሥጋ አልጫ', [], 'mild yellow beef stew with turmeric and ginger, on injera'),
 ('Beg Key Wot', 'የበግ ቀይ ወጥ', ['spicy'], 'spicy red lamb stew with tender bone-in lamb pieces, on injera'),
 ('Beg Alicha', 'የበግ አልጫ', [], 'mild golden lamb stew with green chili, on injera'),
 ('Minchet Abish', 'ምንቸት አብሽ', ['spicy'], 'finely minced beef in a rich red berbere sauce, smooth texture, on injera'),
 ('Yebeg Kikil', 'የበግ ቅቅል', [], 'clear lamb bone broth with tender bone-in lamb, garlic and green chili, in a deep bowl'),
 ('Yesiga Kikil', 'የሥጋ ቅቅል', [], 'light beef broth with bone-in beef chunks, ginger and garlic, in a deep bowl'),
 ('Dulet', 'ዱለት', ['spicy'], 'finely chopped tripe, liver and lean beef fried with butter, onion, mitmita and green chili'),
 ('Gomen Besiga', 'ጎመን በሥጋ', [], 'braised collard greens with tender beef pieces, on injera'),
 ('Asa Wot', 'የአሳ ወጥ', ['spicy'], 'red berbere fish stew with chunks of white fish, on injera'),
 ('Asa Alicha', 'የአሳ አልጫ', [], 'mild golden fish stew with turmeric, on injera'),
 ('Bozena Shiro', 'ቦዘና ሽሮ', ['spicy'], 'thick orange chickpea shiro with small cubes of fried beef, in a black clay pot'),
 ('Doro Wot Special', None, ['spicy'], 'festive doro wot with two drumsticks and two eggs in a black clay pot with injera rolls'),
 ('Yekey Wot Firfir', None, ['spicy'], 'torn injera soaked in red beef stew, piled high on a plate'),
])
add('fasting dishes', [
 ('Shiro Wot', 'ሽሮ ወጥ', ['fasting', 'vegetarian'], 'smooth orange-brown chickpea stew with a glossy oil sheen, on injera'),
 ('Shiro Tegabino', 'ሽሮ ተጋቢኖ', ['fasting', 'vegetarian'], 'thick bubbling chickpea shiro served in a small black clay pot (tegabino), injera rolls beside it'),
 ('Shiro Fitfit', 'ሽሮ ፍትፍት', ['fasting', 'vegetarian'], 'injera pieces mixed into orange shiro with chopped tomato and green chili'),
 ('Misir Wot', 'ምስር ወጥ', ['fasting', 'vegetarian', 'spicy'], 'deep red spicy split red lentil stew, on injera'),
 ('Misir Alicha', 'ምስር አልጫ', ['fasting', 'vegetarian'], 'mild yellow lentil stew with turmeric, on injera'),
 ('Kik Alicha', 'ክክ አልጫ', ['fasting', 'vegetarian'], 'golden yellow split pea stew, smooth and mild, on injera'),
 ('Ater Kik', 'አተር ክክ', ['fasting', 'vegetarian'], 'yellow split peas cooked with garlic and turmeric, on injera'),
 ('Atkilt Wot', 'አትክልት ወጥ', ['fasting', 'vegetarian'], 'cabbage, carrot and potato stewed with turmeric, golden yellow, on injera'),
 ('Gomen', 'ጎመን', ['fasting', 'vegetarian'], 'dark green braised collard greens with garlic and green chili, on injera'),
 ('Fosolia', 'ፎሶሊያ', ['fasting', 'vegetarian'], 'green beans and carrot strips sautéed with onion, on injera'),
 ('Tikil Gomen', 'ጥቅል ጎመን', ['fasting', 'vegetarian'], 'cabbage, carrot and potato sautéed with turmeric and ginger'),
 ('Dinich Wot', 'ድንች ወጥ', ['fasting', 'vegetarian', 'spicy'], 'potato chunks in red berbere sauce, on injera'),
 ('Azifa', 'አዚፋ', ['fasting', 'vegetarian'], 'cold green lentil salad with mustard, red onion, green chili and lemon'),
 ('Timatim Salata', 'ቲማቲም ሰላጣ', ['fasting', 'vegetarian'], 'fresh chopped tomato, red onion and green chili salad with lemon'),
 ('Timatim Fitfit', 'ቲማቲም ፍትፍት', ['fasting', 'vegetarian'], 'torn injera mixed with fresh tomato, onion and green chili'),
 ('Butecha', 'ቡጥቻ', ['fasting', 'vegetarian'], 'pale yellow crumbly chickpea mash with green chili and onion'),
 ('Shimbra Asa', 'ሽምብራ አሳ', ['fasting', 'vegetarian', 'spicy'], 'fried chickpea dumplings in a red berbere sauce'),
 ('Inguday Tibs', 'እንጉዳይ ጥብስ', ['fasting', 'vegetarian'], 'sautéed sliced mushrooms with onion, tomato and green chili'),
 ('Yetsom Beyaynetu', 'የጾም በያይነቱ', ['fasting', 'vegetarian'], 'large round injera topped with many small colourful mounds: shiro, misir, kik, gomen, atkilt, fosolia, salad'),
 ('Suff Fitfit', 'ሱፍ ፍትፍት', ['fasting', 'vegetarian'], 'injera soaked in creamy white sunflower seed drink, cold'),
 ('Yetsom Firfir', 'የጾም ፍርፍር', ['fasting', 'vegetarian', 'spicy'], 'torn injera fried with red berbere sauce, onion and oil, no meat'),
 ('Fasting Pasta', None, ['fasting', 'vegetarian'], 'spaghetti in a bright tomato sauce with vegetables, Addis fasting style'),
 ('Ful Medames', 'ፉል', ['fasting', 'vegetarian'], 'mashed fava beans topped with chopped tomato, onion, green chili, olive oil, with bread roll'),
 ('Special Ful', 'ስፔሻል ፉል', ['vegetarian'], 'fava bean ful topped with fried egg, yoghurt, tomato, onion and chili, with bread'),
 ('Ful with Egg', None, ['vegetarian'], 'mashed fava beans with a boiled egg chopped on top, chili and onion, bread roll'),
 ('Mahberawi Fasting Combo', None, ['fasting', 'vegetarian'], 'injera platter with eight different fasting stews arranged in a circle'),
 ('Kik Wot', 'ክክ ወጥ', ['fasting', 'vegetarian', 'spicy'], 'split peas in red berbere sauce, on injera'),
 ('Gomen Kitfo', 'ጎመን ክትፎ', ['fasting', 'vegetarian'], 'finely chopped dark green collards with spiced butter flavour and ayib-style crumble, Gurage style'),
])
add('raw and minced meat', [
 ('Kitfo', 'ክትፎ', [], 'finely minced raw beef glistening with spiced butter and mitmita, on a small plate'),
 ('Kitfo Leb Leb', 'ክትፎ ለብለብ', [], 'minced beef lightly warmed in spiced butter, pink inside'),
 ('Special Kitfo', 'ስፔሻል ክትፎ', [], 'kitfo served with ayib cheese, braised gomen and kocho bread on a woven platter'),
 ('Kitfo with Kocho', 'ክትፎ በቆጮ', [], 'minced beef with flat ensete kocho bread and a bowl of mitmita'),
 ('Gored Gored', 'ጎረድ ጎረድ', [], 'cubes of raw beef tossed in spiced butter and awaze'),
 ('Kurt', 'ቁርጥ', [], 'large slices of fresh raw beef on a wooden board with awaze and mitmita dips'),
 ('Tere Siga Platter', 'ጥሬ ሥጋ', [], 'raw beef cut into strips on a board with a knife, awaze and mitmita'),
 ('Dulet Special', None, ['spicy'], 'dulet with ayib cheese and injera rolls on the side'),
 ('Kitfo Fitfit', None, [], 'injera pieces mixed with kitfo and spiced butter'),
 ('Kitfo Sandwich', None, [], 'soft bread roll filled with spiced minced beef'),
])
add('tibs', [
 ('Derek Tibs', 'ደረቅ ጥብስ', [], 'dry-fried beef cubes with onion, rosemary and green chili'),
 ('Lega Tibs', 'ለጋ ጥብስ', [], 'tender beef cubes sautéed with tomato, onion and green chili, juicy'),
 ('Awaze Tibs', 'አዋዜ ጥብስ', ['spicy'], 'beef cubes in red awaze chili paste with onion'),
 ('Zilzil Tibs', 'ዝልዝል ጥብስ', [], 'long strips of beef fried crisp with onion and green chili'),
 ('Shekla Tibs', 'ሸክላ ጥብስ', [], 'sizzling meat served in a clay pot with burning coals underneath, rosemary on top'),
 ('Yebeg Tibs', 'የበግ ጥብስ', [], 'sautéed lamb cubes with onion, rosemary and green chili'),
 ('Yefiyel Tibs', 'የፍየል ጥብስ', [], 'sautéed goat meat with onion and rosemary'),
 ('Doro Tibs', 'የዶሮ ጥብስ', [], 'chicken pieces sautéed with onion, tomato and rosemary'),
 ('Asa Tibs', 'የአሳ ጥብስ', [], 'fried fish cubes with onion, tomato and green chili'),
 ('Tibs Firfir', 'ጥብስ ፍርፍር', ['spicy'], 'torn injera mixed with sautéed beef tibs and berbere sauce'),
 ('Special Tibs', None, [], 'mixed tibs platter with rosemary sprigs and injera rolls'),
 ('Gomen Tibs', None, [], 'beef tibs with braised collard greens'),
 ('Tibs with Rice', None, [], 'sautéed beef tibs next to white rice and salad'),
 ('Chicken Tibs Special', None, [], 'chicken tibs in a hot clay pot with peppers'),
 ('Yebeg Shekla Tibs', None, [], 'lamb tibs in a clay pot over hot coals'),
])
add('breakfast', [
 ('Firfir', 'ፍርፍር', ['spicy'], 'shredded injera tossed in red berbere sauce and butter, served hot'),
 ('Chechebsa', 'ጨጨብሳ', [], 'torn crispy flatbread coated in spiced butter and berbere, with honey and yoghurt on the side'),
 ('Kinche', 'ቅንጬ', ['vegetarian'], 'cracked wheat cooked with spiced butter, fluffy, in a bowl'),
 ('Genfo', 'ገንፎ', ['vegetarian'], 'thick barley porridge with a well of spiced butter and berbere in the middle'),
 ('Enkulal Firfir', 'እንቁላል ፍርፍር', ['vegetarian'], 'scrambled eggs with tomato, onion and green chili'),
 ('Enkulal Tibs', 'እንቁላል ጥብስ', ['vegetarian'], 'eggs fried with onion, tomato and jalapeño'),
 ('Quanta Firfir', 'ቋንጣ ፍርፍር', ['spicy'], 'injera firfir with pieces of dried beef jerky in red sauce'),
 ('Kategna', 'ቃተኛ', ['vegetarian', 'spicy'], 'toasted injera brushed with spiced butter and berbere, cut into triangles'),
 ('Fetira', 'ፈጢራ', ['vegetarian'], 'layered flaky flatbread with egg, honey drizzle'),
 ('Fetira with Honey', None, ['vegetarian'], 'crispy folded fetira with honey and powdered sugar'),
 ('Chechebsa with Honey', None, ['vegetarian'], 'chechebsa topped with golden honey'),
 ('Dulet Breakfast', None, ['spicy'], 'dulet with a bread roll and tea'),
 ('Ful Special Breakfast', None, ['vegetarian'], 'ful with fried egg, bread, and tea'),
 ('Atmit', 'አጥሚት', ['vegetarian'], 'warm smooth oat and barley drink-porridge in a cup'),
 ('Ambasha Breakfast', None, ['vegetarian'], 'sliced ambasha bread with butter, honey and tea'),
])
add('bread', [
 ('Injera', 'እንጀራ', ['fasting', 'vegetarian'], 'large round spongy teff injera folded and rolled, showing its eyes (holes)'),
 ('Teff Injera Rolls', None, ['fasting', 'vegetarian'], 'rolled injera pieces stacked on a plate'),
 ('Ambasha', 'አምባሻ', ['vegetarian'], 'round spiced festive bread with a decorated wheel pattern on top'),
 ('Himbasha', 'ሕምባሻ', ['vegetarian'], 'round sweet bread scored into a wheel pattern, golden crust'),
 ('Defo Dabo', 'ድፎ ዳቦ', ['vegetarian'], 'large round thick wheat loaf baked in leaves, sliced'),
 ('Dabo', 'ዳቦ', ['vegetarian'], 'soft white bread rolls in a basket'),
 ('Kita', 'ቂጣ', ['vegetarian'], 'thin unleavened flatbread, lightly charred'),
 ('Kocho', 'ቆጮ', ['vegetarian'], 'flat ensete (false banana) bread, dense and pale'),
 ('Bula Porridge', 'ቡላ', ['vegetarian'], 'smooth white ensete porridge with butter'),
 ('Anebabero', 'አነባበሮ', ['vegetarian'], 'layered injera with butter and berbere between layers'),
 ('Dabo Kolo', 'ዳቦ ቆሎ', ['vegetarian'], 'small crunchy spiced bread nuggets in a bowl'),
 ('Kolo', 'ቆሎ', ['vegetarian'], 'roasted barley and chickpea snack mix in a woven basket'),
 ('Sambusa Lentil', 'ሳምቡሳ', ['fasting', 'vegetarian'], 'crispy triangular pastries filled with spiced lentils'),
 ('Sambusa Beef', None, [], 'crispy triangular pastries filled with minced beef'),
 ('Bread with Butter and Honey', None, ['vegetarian'], 'sliced white bread with butter and golden honey'),
])
add('drinks (traditional)', [
 ('Buna (Ethiopian Coffee)', 'ቡና', ['vegetarian'], 'black coffee poured from a clay jebena into small handleless cups, frankincense smoke'),
 ('Coffee Ceremony', None, ['vegetarian'], 'jebena coffee pot, tiny cups on a tray, popcorn and grass, incense'),
 ('Macchiato', 'ማኪያቶ', ['vegetarian'], 'Ethiopian macchiato in a small clear glass with distinct coffee and milk layers'),
 ('Spris (Tea and Coffee)', None, ['vegetarian'], 'layered glass of half tea, half coffee'),
 ('Shai (Spiced Tea)', 'ሻይ', ['vegetarian'], 'small glass of red-brown spiced tea with cinnamon and cloves'),
 ('Tej', 'ጠጅ', [], 'golden honey wine in a traditional round-bellied berele flask'),
 ('Tella', 'ጠላ', [], 'dark home-brewed barley beer in a clay cup'),
 ('Borde', 'ቦርዴ', [], 'thick cloudy fermented grain drink in a gourd cup'),
 ('Ergo', 'እርጎ', ['vegetarian'], 'thick traditional yoghurt in a bowl'),
 ('Ayib', 'አይብ', ['vegetarian'], 'fresh crumbly white Ethiopian cottage cheese'),
 ('Ayib with Mitmita', None, ['vegetarian', 'spicy'], 'crumbly ayib sprinkled with red mitmita powder'),
 ('Besso', 'በሶ', ['vegetarian'], 'barley flour drink, beige and smooth, in a glass'),
 ('Suff Drink', 'ሱፍ', ['fasting', 'vegetarian'], 'creamy white sunflower seed drink in a glass'),
 ('Telba Drink', 'ተልባ', ['fasting', 'vegetarian'], 'brown flaxseed drink in a glass'),
 ('Kenetto', None, ['vegetarian'], 'golden traditional fermented drink in a glass'),
])

# ---------- Families: real menu variations sold in Addis cafés, restaurants, bakeries and juice bars ----------
FAM = []
def fam(cat, base_desc, items, tags=None):
    for it in items:
        name, extra = (it if isinstance(it, tuple) else (it, ''))
        FAM.append((name, None, cat, list(tags or []), (extra or base_desc.format(n=name.lower()))))

fam('coffee and tea', 'cafe {n} in a ceramic cup on a saucer, latte art where fitting', [
 'Espresso', 'Double Espresso', 'Americano', 'Cappuccino', 'Caffe Latte', 'Flat White', 'Cortado', 'Mocha', 'Caramel Macchiato', 'Hazelnut Latte',
 'Vanilla Latte', 'Iced Latte', 'Iced Americano', 'Iced Mocha', 'Affogato', 'Hot Chocolate', 'Chai Latte', 'Matcha Latte', 'Turkish Coffee', 'Coffee with Milk',
 'Black Tea', 'Green Tea', 'Ginger Tea', 'Lemon Tea', 'Mint Tea', 'Tea with Milk', 'Honey Lemon Ginger Tea', 'Hibiscus Tea', 'Iced Tea', 'Peach Iced Tea'], ['vegetarian'])
fresh = ['Avocado', 'Mango', 'Papaya', 'Guava', 'Orange', 'Pineapple', 'Strawberry', 'Banana', 'Watermelon', 'Lemon', 'Carrot', 'Beetroot', 'Passion Fruit', 'Apple', 'Tomato', 'Grape', 'Kiwi', 'Pear', 'Mixed Fruit', 'Spris (Layered)']
fam('juice', 'tall glass of fresh thick {n} with condensation, fruit garnish', [f'{f} Juice' for f in fresh], ['fasting', 'vegetarian'])
fam('juice', 'tall glass of creamy {n}, straw, fruit slice', [f'{f} Smoothie' for f in ['Mango', 'Strawberry', 'Banana', 'Avocado', 'Mixed Berry', 'Papaya', 'Pineapple', 'Peanut Butter Banana', 'Green Detox', 'Oat Banana']], ['vegetarian'])
fam('juice', 'tall glass of thick {n} topped with whipped cream', [f'{f} Milkshake' for f in ['Vanilla', 'Chocolate', 'Strawberry', 'Banana', 'Oreo', 'Caramel', 'Mango', 'Coffee', 'Avocado', 'Peanut']], ['vegetarian'])
fam('juice', '{n} in a glass with ice and fruit', ['Lemonade', 'Mint Lemonade', 'Ginger Lemonade', 'Fresh Coconut Water', 'Sparkling Water with Lemon', 'Avocado and Mango Mix', 'Avocado and Papaya Spris', 'Mango and Orange Mix', 'Strawberry Lemonade', 'Watermelon Mint Cooler'], ['fasting', 'vegetarian'])
pizz = ['Margherita', 'Special', 'Vegetable', 'Tuna', 'Chicken', 'Beef', 'Fasting', 'Pepperoni', 'Hawaiian', 'Mushroom', 'Four Cheese', 'BBQ Chicken', 'Meat Lovers', 'Spicy Beef', 'Seafood', 'Kitfo', 'Shrimp', 'Sausage', 'Pesto Chicken', 'Ethiopian Spiced Chicken']
fam('pizza', 'whole {n} on a wooden board, melted stretchy cheese, blistered crust', [f'{p} Pizza' for p in pizz])
fam('pizza', 'single slice of {n} lifted with a cheese pull', [f'{p} Pizza Slice' for p in pizz[:10]])
burg = ['Classic Beef', 'Cheese', 'Double Cheese', 'Chicken', 'Crispy Chicken', 'Fish', 'Vegetable', 'Mushroom Swiss', 'BBQ Bacon', 'Egg', 'Spicy Awaze Beef', 'Special', 'Lamb', 'Tuna', 'Fasting Veggie']
fam('burgers and sandwiches', 'juicy {n} with sesame bun, lettuce, tomato, side of golden fries', [f'{b} Burger' for b in burg])
sand = ['Club', 'Tuna', 'Chicken', 'Egg', 'Vegetable', 'Cheese', 'Beef', 'Grilled Cheese', 'Chicken Avocado', 'Steak', 'BLT', 'Falafel', 'Shawarma Chicken', 'Shawarma Beef', 'Panini Caprese']
fam('burgers and sandwiches', '{n} cut in half showing layers, with fries', [f'{s} Sandwich' for s in sand])
fam('burgers and sandwiches', '{n}, golden, sliced, on a board', ['Chicken Wrap', 'Beef Wrap', 'Veggie Wrap', 'Falafel Wrap', 'Tuna Wrap', 'Hot Dog', 'Chicken Quesadilla', 'Beef Quesadilla', 'Chicken Burrito', 'Beef Tacos'])
pasta = ['Spaghetti Bolognese', 'Spaghetti Tomato Sauce', 'Spaghetti with Tuna', 'Penne Arrabbiata', 'Fettuccine Alfredo', 'Chicken Alfredo', 'Lasagna', 'Vegetable Lasagna', 'Macaroni with Meat Sauce', 'Macaroni and Cheese',
 'Penne with Chicken', 'Spaghetti Carbonara', 'Pesto Pasta', 'Seafood Pasta', 'Shrimp Pasta', 'Spaghetti Aglio Olio', 'Creamy Mushroom Pasta', 'Baked Penne', 'Ravioli', 'Gnocchi in Tomato Sauce']
fam('pasta and rice', 'plate of {n}, garnished with parmesan and basil', pasta)
rice = ['Vegetable Fried Rice', 'Chicken Fried Rice', 'Beef Fried Rice', 'Rice with Vegetables', 'Rice with Beef Sauce', 'Rice with Chicken', 'Biryani Chicken', 'Biryani Lamb', 'Jollof-style Rice', 'Rice with Tibs', 'Shrimp Fried Rice', 'Egg Fried Rice', 'Rice and Beans', 'Pilau Rice', 'Rice with Fish']
fam('pasta and rice', 'plate of {n}, colourful, steam rising', rice)
grill = ['Mixed Grill', 'Beef Steak', 'Pepper Steak', 'T-bone Steak', 'Lamb Chops', 'Grilled Chicken', 'Half Grilled Chicken', 'Chicken Wings', 'BBQ Chicken Wings', 'Spicy Chicken Wings', 'Chicken Kebab', 'Beef Kebab', 'Lamb Kebab', 'Kofta Kebab', 'Grilled Sausages',
 'Beef Ribs', 'Chicken Skewers', 'Lamb Shoulder', 'Roast Chicken', 'Chicken Schnitzel', 'Beef Schnitzel', 'Fried Chicken', 'Chicken Nuggets', 'Chicken Strips', 'Chicken Gulash', 'Beef Gulash', 'Lamb Stew', 'Roast Beef', 'Grilled Liver', 'Mixed Kebab Platter']
fam('grill and meat', '{n} on a cast iron plate, grill marks, charred edges, herbs', grill)
fish = ['Fried Fish (Asa Lebleb)', 'Whole Fried Tilapia', 'Grilled Tilapia', 'Fish Gulash', 'Fish Cutlet', 'Fish and Chips', 'Grilled Nile Perch', 'Fish Goulash with Rice', 'Fried Fish Fillet', 'Garlic Shrimp', 'Grilled Prawns', 'Calamari Rings', 'Fish Burger Platter', 'Fish Tibs Platter', 'Lake Tana Fish Platter']
fam('fish', '{n}, crispy golden, lemon wedges and fresh salad', fish)
soup = ['Lentil Soup', 'Vegetable Soup', 'Chicken Soup', 'Mushroom Soup', 'Tomato Soup', 'Pumpkin Soup', 'Beef Soup', 'Lamb Soup', 'Fish Soup', 'Minestrone', 'Cream of Chicken', 'Potato Leek Soup', 'Carrot Ginger Soup', 'Bone Broth', 'Spicy Lentil Soup']
fam('soups and salads', 'bowl of {n} with bread on the side, steam rising', soup)
salad = ['Garden Salad', 'Greek Salad', 'Caesar Salad', 'Chicken Caesar Salad', 'Tuna Salad', 'Avocado Salad', 'Mixed Salad', 'Pasta Salad', 'Potato Salad', 'Beetroot Salad', 'Coleslaw', 'Fruit Salad', 'Chicken Salad', 'Quinoa Salad', 'Tomato and Avocado Salad']
fam('soups and salads', 'fresh {n} in a white bowl, crisp and colourful', salad)
sides = ['French Fries', 'Spicy Fries', 'Potato Wedges', 'Sweet Potato Fries', 'Mashed Potatoes', 'Boiled Potatoes', 'Roasted Vegetables', 'Steamed Vegetables', 'Garlic Bread', 'Onion Rings', 'Fried Plantain', 'Boiled Corn', 'Roasted Corn (Bekolo)', 'Boiled Sweet Potato', 'Spring Rolls',
 'Samosa Vegetable', 'Falafel', 'Hummus with Pita', 'Fried Egg', 'Boiled Eggs', 'Omelette Plain', 'Vegetable Omelette', 'Cheese Omelette', 'Spanish Omelette', 'Egg Sandwich Toast', 'Pancakes', 'Pancakes with Honey', 'French Toast', 'Waffles', 'Crepe with Chocolate']
fam('sides and breakfast (café)', 'portion of {n} on a plate, golden and appetising', sides, ['vegetarian'])
cakes = ['Chocolate Cake', 'Black Forest Cake', 'Red Velvet Cake', 'Carrot Cake', 'Cheesecake', 'Strawberry Cheesecake', 'Vanilla Sponge Cake', 'Lemon Cake', 'Banana Bread', 'Coffee Cake', 'Fruit Cake', 'Tiramisu', 'Opera Cake', 'Coconut Cake', 'Caramel Cake',
 'Birthday Cake', 'Chocolate Fudge Cake', 'Mango Mousse Cake', 'Oreo Cake', 'Marble Cake', 'Cupcake Vanilla', 'Cupcake Chocolate', 'Brownie', 'Blondie', 'Cookies Chocolate Chip', 'Oatmeal Cookies', 'Butter Biscuits', 'Macarons', 'Eclair', 'Mille-feuille',
 'Croissant', 'Chocolate Croissant', 'Almond Croissant', 'Cinnamon Roll', 'Danish Pastry', 'Doughnut Glazed', 'Doughnut Chocolate', 'Bombolino', 'Muffin Blueberry', 'Muffin Chocolate', 'Apple Pie', 'Fruit Tart', 'Lemon Tart', 'Baklava', 'Basbousa',
 'Cream Puff', 'Swiss Roll', 'Scone', 'Pain au Raisin', 'Mini Pastry Assortment']
fam('cakes and pastries', 'slice or piece of {n} on a small plate, bakery display quality', cakes, ['vegetarian'])
desserts = ['Vanilla Ice Cream', 'Chocolate Ice Cream', 'Strawberry Ice Cream', 'Mango Ice Cream', 'Ice Cream Sundae', 'Banana Split', 'Fruit Salad with Ice Cream', 'Creme Caramel', 'Chocolate Mousse', 'Panna Cotta',
 'Rice Pudding', 'Yoghurt with Honey', 'Yoghurt Parfait', 'Frozen Yoghurt', 'Gelato Trio']
fam('desserts', '{n} in a glass bowl, beautifully plated', desserts, ['vegetarian'])
fast = ['Shawarma Chicken Plate', 'Shawarma Beef Plate', 'Chicken Shawarma Roll', 'Beef Shawarma Roll', 'Falafel Plate', 'Kebab Plate', 'Loaded Fries', 'Cheese Fries', 'Chicken Popcorn', 'Fish Fingers',
 'Mozzarella Sticks', 'Nachos', 'Chicken Nachos', 'Corn Dog', 'Sausage Roll', 'Meat Pie', 'Chicken Pie', 'Vegetable Pie', 'Calzone', 'Garlic Knots']
fam('fast food', '{n} served in a paper-lined basket, golden, freshly made', fast)
asian = ['Chicken Noodles', 'Beef Noodles', 'Vegetable Noodles', 'Sweet and Sour Chicken', 'Kung Pao Chicken', 'Beef Stir Fry', 'Chicken Curry', 'Vegetable Curry', 'Lamb Curry', 'Butter Chicken',
 'Chicken Tikka', 'Dal Tadka', 'Chapati', 'Naan Bread', 'Spring Roll Platter']
fam('international', 'plate of {n}, restaurant plating', asian)
breakfast_int = ['Full Breakfast', 'Eggs Benedict', 'Avocado Toast', 'Avocado Toast with Egg', 'Granola Bowl', 'Oatmeal with Fruit', 'Toast with Jam', 'Cheese Toast', 'Sausage and Eggs', 'Breakfast Burrito']
fam('sides and breakfast (café)', '{n} on a plate, morning light', breakfast_int)


# ---------- More real items (regional Ethiopian, Addis menus, bars, bakeries) ----------
add('regional', [
 ('Tihlo', 'ጥሕሎ', [], 'Tigrayan roasted barley dough balls dipped with a wooden stick into a spicy meat sauce'),
 ('Kitcha Fitfit', None, ['vegetarian'], 'torn unleavened flatbread tossed in spiced butter and berbere, yoghurt on the side'),
 ('Zigni', None, ['spicy'], 'Tigrinya-style spicy red beef stew, on injera'),
 ('Shahan Ful', None, ['vegetarian'], 'mashed fava beans topped with yoghurt, tomato, onion and green chili, with bread'),
 ('Chiko', 'ጭኮ', ['vegetarian'], 'Sidama roasted barley flour mixed with spiced butter, pressed into a block'),
 ('Marqa', None, ['vegetarian'], 'Oromo-style thick porridge with butter and spices'),
 ('Ga’at', None, ['vegetarian'], 'Tigrinya barley porridge with butter and berbere in the centre, yoghurt ring'),
 ('Hilbet', None, ['fasting', 'vegetarian'], 'smooth whipped lentil and fenugreek paste, served with injera'),
 ('Silsi', None, ['fasting', 'vegetarian', 'spicy'], 'spicy tomato and onion berbere sauce, glossy red'),
 ('Kurkufa', None, ['vegetarian'], 'barley dumplings in a spiced butter sauce'),
 ('Ambasha Tigray Style', None, ['vegetarian'], 'large round decorated wheat bread with incised pattern'),
 ('Kocho with Ayib', None, ['vegetarian'], 'ensete bread with fresh ayib cheese and spiced butter'),
 ('Gurage Gomen with Ayib', None, ['vegetarian'], 'chopped collards with fresh ayib cheese, Gurage style'),
 ('Harari Hulbet Merek', None, ['spicy'], 'Harari-style meat stew topped with whipped fenugreek'),
 ('Asa Lebleb', 'አሳ ለብለብ', [], 'lightly fried fish pieces with onion and green chili'),
])
fam('beer and drinks (bar)', 'chilled {n} in a glass, condensation, generic unbranded label', [
 'Local Lager Beer', 'Draft Beer', 'Dark Beer', 'Malt Beer', 'Non-alcoholic Beer', 'Red Wine (Ethiopian)', 'White Wine (Ethiopian)', 'Rosé Wine', 'Areki', 'Gin and Tonic',
 'Whisky on the Rocks', 'Vodka with Juice', 'Mojito (Virgin)', 'Pina Colada (Virgin)', 'Sangria (Non-alcoholic)'])
fam('bakery', 'fresh {n} on a wooden board, bakery light', [
 'Baguette', 'Brown Bread', 'Whole Wheat Bread', 'Sourdough Loaf', 'Ciabatta', 'Bagel', 'Pita Bread', 'Burger Buns', 'Sliced White Bread', 'Milk Bread',
 'Sesame Bread Roll', 'Raisin Bread', 'Focaccia', 'Breadsticks', 'Cheese Bread'], ['vegetarian'])
fam('sides and breakfast (café)', '{n} on a plate, morning light', [
 'Scrambled Eggs', 'Poached Eggs on Toast', 'Sunny Side Up Eggs', 'Eggs with Sausage', 'Eggs with Tomato', 'Egg and Cheese Muffin', 'Shakshuka', 'Hash Browns', 'Baked Beans on Toast', 'Breakfast Platter',
 'Yoghurt with Granola', 'Honey Toast', 'Peanut Butter Toast', 'Banana Pancakes', 'Chocolate Pancakes'], ['vegetarian'])
fam('coffee and tea', 'cafe {n}, beautifully served', [
 'Cold Brew', 'Iced Caramel Latte', 'Caramel Frappe', 'Mocha Frappe', 'Vanilla Frappe', 'Espresso Macchiato', 'Ristretto', 'Spiced Coffee with Cardamom', 'Coffee with Butter (Kuti)', 'Iced Macchiato',
 'White Mocha', 'Cinnamon Latte', 'Honey Latte', 'Oat Milk Latte', 'Decaf Coffee'], ['vegetarian'])
fam('juice', 'tall glass of layered {n}, vivid colours', [
 'Avocado and Orange Spris', 'Mango and Papaya Spris', 'Strawberry and Banana Juice', 'Avocado and Strawberry Spris', 'Guava and Mango Mix', 'Papaya and Lime Juice', 'Pineapple and Ginger Juice', 'Carrot and Orange Juice', 'Beetroot and Apple Juice', 'Watermelon and Lime Juice',
 'Mango Lassi', 'Sweet Lassi', 'Fresh Sugarcane Juice', 'Tamarind Juice', 'Hibiscus Cooler'], ['vegetarian'])
fam('fruit', 'fresh {n} beautifully cut and plated', [
 'Fruit Platter', 'Mango Slices', 'Papaya with Lime', 'Watermelon Slices', 'Pineapple Slices', 'Avocado Half', 'Banana Bunch', 'Orange Wedges', 'Strawberries Bowl', 'Mixed Berries Bowl',
 'Guava Halves', 'Grapes Bunch', 'Apple Slices', 'Fruit Skewers', 'Tropical Fruit Bowl'], ['fasting', 'vegetarian'])
fam('snacks', '{n} in a bowl, appetising', [
 'Popcorn', 'Roasted Peanuts', 'Potato Crisps', 'Cassava Chips', 'Plantain Chips', 'Mixed Nuts', 'Roasted Chickpeas', 'Cheese and Crackers', 'Olives Bowl', 'Chicken Lollipops',
 'Meatballs', 'Mini Sliders', 'Chicken Croquettes', 'Vegetable Pakora', 'Bruschetta'])
fam('kids menu', 'kid-sized {n} on a colourful plate', [
 'Kids Burger', 'Kids Pasta', 'Kids Chicken Nuggets', 'Kids Pizza', 'Kids Fish Fingers', 'Kids Fries', 'Kids Pancakes', 'Kids Sandwich', 'Kids Rice and Chicken', 'Kids Ice Cream'])
fam('grill and meat', '{n} on a plate, juicy and well seared', [
 'Chicken Leg Quarter', 'Grilled Chicken Breast', 'Chicken Shish Tawook', 'Lamb Tibs Platter', 'Beef Brochette', 'Peri-Peri Chicken', 'Lemon Herb Chicken', 'Honey Glazed Chicken', 'Garlic Butter Steak', 'Steak and Fries',
 'Pork-free Beef Sausage Platter', 'Grilled Goat', 'Roast Lamb Leg', 'Chicken Tenders Platter', 'Mixed Meat Platter for Two'])
fam('international', 'plate of {n}, restaurant plating', [
 'Beef Lasagna Slice', 'Moussaka', 'Paella', 'Risotto Mushroom', 'Chicken Fajitas', 'Beef Fajitas', 'Chilli con Carne', 'Couscous with Vegetables', 'Lamb Tagine', 'Chicken Tagine',
 'Beef Stroganoff', 'Chicken Cordon Bleu', 'Fish Curry', 'Chicken Biryani Platter', 'Vegetable Stir Fry', 'Teriyaki Chicken', 'Sushi Platter', 'Pad Thai', 'Ramen', 'Dumplings'])
fam('soups and salads', 'bowl of {n}, fresh', [
 'Chickpea Salad', 'Lentil Salad', 'Cucumber Salad', 'Cabbage Salad', 'Rocket and Parmesan Salad', 'Fattoush', 'Tabbouleh', 'Nicoise Salad', 'Mango Avocado Salad', 'Grilled Chicken Salad',
 'Egg Salad', 'Bean Salad', 'Corn Salad', 'Beef Salad', 'Seafood Salad'])
fam('desserts', '{n}, beautifully plated', [
 'Chocolate Lava Cake', 'Cheesecake Slice with Berries', 'Profiteroles', 'Creme Brulee', 'Pavlova', 'Trifle', 'Bread Pudding', 'Sticky Toffee Pudding', 'Mango Pudding', 'Coconut Pudding',
 'Honey Cake', 'Halva', 'Kunafa', 'Mahalabia', 'Waffle with Ice Cream'], ['vegetarian'])
fam('pasta and rice', 'plate of {n}, garnished', [
 'Spaghetti Meatballs', 'Penne Vodka Sauce', 'Linguine Clams', 'Tortellini', 'Mac and Cheese Bake', 'Rigatoni Beef Ragu', 'Spinach Ricotta Cannelloni', 'Tuna Penne Bake', 'Vegetable Pasta Primavera', 'Chicken Pesto Penne'])


add('tibs', [
 ('Derek Tibs', 'ደረቅ ጥብስ', [], 'dry crispy beef tibs with rosemary and green chili, in a clay dish'),
 ('Lega Tibs', 'ለጋ ጥብስ', [], 'tender lightly cooked beef cubes with onion and green chili'),
 ('Shekla Tibs', 'ሸክላ ጥብስ', [], 'sizzling beef tibs served in a clay pot with burning coals underneath'),
 ('Zilzil Tibs', 'ዝልዝል ጥብስ', [], 'long strips of beef fried with awaze, onion and rosemary'),
 ('Beg Tibs', 'የበግ ጥብስ', [], 'lamb tibs with onion, rosemary and jalapeño'),
 ('Fyel Tibs', 'የፍየል ጥብስ', [], 'goat tibs with onion and green chili, rustic plate'),
 ('Doro Tibs', 'ዶሮ ጥብስ', [], 'chicken tibs with onion, tomato and green chili'),
 ('Gored Gored', 'ጎረድ ጎረድ', [], 'raw cubed beef tossed in spiced butter and awaze'),
 ('Dulet', 'ዱለት', ['spicy'], 'minced tripe, liver and lean beef with spiced butter and mitmita'),
 ('Quanta Firfir', 'ቋንጣ ፍርፍር', ['spicy'], 'dried beef strips with torn injera in berbere sauce'),
 ('Quanta Wot', 'ቋንጣ ወጥ', ['spicy'], 'dried beef stew in deep red berbere sauce'),
 ('Ribs Tibs', None, [], 'beef ribs fried with onion, rosemary and green chili'),
 ('Awaze Tibs', 'አዋዜ ጥብስ', ['spicy'], 'beef tibs coated in red awaze paste, onion and pepper'),
 ('Gomen Besiga', 'ጎመን በስጋ', [], 'collard greens cooked with beef pieces'),
 ('Dinich Besiga', 'ድንች በስጋ', [], 'potato and beef stew in a mild sauce'),
])
add('fasting dishes', [
 ('Atkilt Tibs', None, ['fasting', 'vegetarian'], 'sautéed carrots, cabbage, potato and onion with green chili'),
 ('Mushroom Tibs', None, ['fasting', 'vegetarian'], 'sautéed mushrooms with onion, tomato and rosemary'),
 ('Shiro Tegabino', 'ሽሮ ተጋቢኖ', ['fasting', 'vegetarian'], 'thick bubbling shiro served in a small clay pot'),
 ('Bozena Shiro', 'ቦዘና ሽሮ', [], 'shiro stew with small pieces of dried or fresh beef'),
 ('Fosolia', 'ፎሶሊያ', ['fasting', 'vegetarian'], 'green beans and carrots sautéed with onion'),
 ('Key Sir', 'ቀይ ስር', ['fasting', 'vegetarian'], 'boiled beetroot and potato with onion and green chili'),
 ('Timatim Fitfit', 'ቲማቲም ፍትፍት', ['fasting', 'vegetarian'], 'fresh tomato, onion, chili and torn injera salad'),
 ('Azifa', 'አዚፋ', ['fasting', 'vegetarian'], 'cold green lentil salad with mustard, onion and chili'),
 ('Butecha', 'ቡጥቻ', ['fasting', 'vegetarian'], 'crumbly chickpea flour mixed with lemon, onion and chili'),
 ('Suf Fitfit', 'ሱፍ ፍትፍት', ['fasting', 'vegetarian'], 'injera soaked in creamy sunflower seed drink with chili'),
 ('Telba Fitfit', 'ተልባ ፍትፍት', ['fasting', 'vegetarian'], 'injera soaked in flaxseed sauce'),
 ('Engudai Wot', None, ['fasting', 'vegetarian'], 'mushroom stew in berbere sauce'),
 ('Ye Duba Wot', 'የዱባ ወጥ', ['fasting', 'vegetarian'], 'pumpkin stew with onion and turmeric'),
 ('Dinich Wot', 'ድንች ወጥ', ['fasting', 'vegetarian'], 'spicy red potato stew'),
 ('Fasting Pasta', None, ['fasting', 'vegetarian'], 'spaghetti in a red tomato and berbere sauce, Ethiopian style'),
])
fam('cakes and pastries', '{n} on a café plate, warm light', [
 'Sambusa with Lentils', 'Sambusa with Meat', 'Bombolino', 'Pasti', 'Kek (Sponge Cake Slice)', 'Donut Ethiopian Style', 'Cream Cake Slice', 'Mille-feuille', 'Chocolate Eclair', 'Fruit Tart',
 'Cinnamon Roll', 'Croissant', 'Chocolate Croissant', 'Almond Croissant', 'Danish Pastry', 'Muffin Blueberry', 'Muffin Chocolate', 'Banana Bread Slice', 'Carrot Cake Slice', 'Lemon Cake Slice',
 'Brownie', 'Cookies Plate', 'Macarons', 'Cupcake Vanilla', 'Cupcake Chocolate'], ['vegetarian'])
fam('coffee and tea', 'cup of {n}, steam rising', [
 'Spiced Tea (Shai)', 'Tea with Milk', 'Ginger Tea', 'Lemon Tea', 'Mint Tea', 'Green Tea', 'Black Tea', 'Hot Chocolate', 'Malted Milk Drink', 'Hot Milk with Honey',
 'Besso Drink', 'Atmit', 'Kinche Tea Set', 'Coffee Ceremony Set', 'Chai Latte'], ['vegetarian'])
fam('fish', '{n}, beautifully plated', [
 'Lake Tana Tilapia Fried', 'Whole Grilled Tilapia', 'Nile Perch Fillet', 'Fish Cutlet', 'Fish and Chips', 'Fish Burger', 'Fish Sandwich', 'Fish Soup', 'Garlic Shrimp', 'Calamari Rings',
 'Grilled Prawns', 'Shrimp Pasta', 'Seafood Rice', 'Fish Tacos', 'Crispy Fried Fish Fillet'], ['fasting'])
fam('wraps and street food', '{n}, freshly made', [
 'Chechebsa Wrap', 'Shawarma Beef', 'Shawarma Chicken', 'Falafel Plate', 'Hummus with Pita', 'Kebab Wrap', 'Chicken Kati Roll', 'Egg Roll', 'Hot Dog', 'Corn Dog',
 'Loaded Fries', 'Cheese Fries', 'Chicken Wings Buffalo', 'Chicken Wings BBQ', 'Mozzarella Sticks', 'Onion Rings', 'Nachos', 'Quesadilla Chicken', 'Burrito Beef', 'Taco Plate'])


fam('bowls and healthy', '{n} in a wide bowl, fresh and colourful', [
 'Chicken Rice Bowl', 'Beef Rice Bowl', 'Tuna Poke Bowl', 'Salmon Poke Bowl', 'Quinoa Bowl', 'Falafel Bowl', 'Avocado Toast with Egg', 'Overnight Oats', 'Acai Bowl', 'Chia Pudding',
 'Smoothie Bowl Mango', 'Smoothie Bowl Berry', 'Grilled Halloumi Salad', 'Teff Porridge Bowl', 'Oatmeal with Banana'])
fam('breakfast', '{n} on a café plate', [
 'Enkulal Firfir with Bread', 'Enkulal Be Siga', 'Chechebsa with Honey', 'Fetira with Egg and Honey', 'Ful with Egg', 'Ful with Avocado', 'Special Ful', 'Kategna with Ayib', 'Dabo Firfir', 'Injera Firfir with Egg'], [])
fam('grill and meat', '{n} on a grill platter', [
 'Beef Kebab Skewers', 'Chicken Kebab Skewers', 'Lamb Kebab Skewers', 'Liver Skewers', 'Grilled Kidney', 'Grilled Sausages', 'Lamb Ribs', 'Beef Short Ribs', 'Chicken Gizzards Fried', 'Grilled Corn on the Cob',
 'Roast Potatoes', 'Grilled Vegetables Platter', 'Kofta Plate', 'Adana Kebab', 'Iskender Kebab'])
fam('sauces and dips', 'small bowl of {n} on a wooden board', [
 'Awaze Dip', 'Mitmita Dip', 'Senafich (Ethiopian Mustard)', 'Garlic Sauce', 'Tahini Sauce', 'Guacamole', 'Salsa', 'BBQ Sauce', 'Chili Sauce', 'Yoghurt Dip'], ['vegetarian'])
fam('desserts', '{n}, frosty and beautifully served', [
 'Vanilla Ice Cream', 'Chocolate Ice Cream', 'Strawberry Ice Cream', 'Mango Sorbet', 'Lemon Sorbet', 'Banana Split', 'Ice Cream Sundae', 'Affogato', 'Frozen Yoghurt', 'Gelato Trio'], ['vegetarian'])


fam('soft drinks', 'chilled {n}, condensation, generic unbranded bottle', [
 'Sparkling Mineral Water', 'Still Bottled Water', 'Tonic Water', 'Ginger Ale', 'Iced Tea Lemon', 'Iced Tea Peach', 'Energy Drink'], ['fasting', 'vegetarian'])

# Ethiopian combos and serving styles that menus list as separate items
combo = [('Beyaynetu (Meat and Fasting)', 'በያይነቱ', [], 'injera platter with doro wot, key wot, tibs, shiro, misir, gomen and salad in a circle'),
 ('Mahberawi Special', 'ማኅበራዊ', [], 'large shared injera platter with kitfo, tibs, doro wot and vegetables'),
 ('Yefisik Beyaynetu', None, [], 'meat combination platter: key wot, alicha, tibs and kitfo on injera'),
 ('Kitfo Combo', None, [], 'kitfo with ayib, gomen, kocho and mitmita on a woven mesob tray'),
 ('Tibs Combo', None, [], 'derek tibs and lega tibs with salad and injera'),
 ('Shiro and Tibs Combo', None, ['spicy'], 'shiro pot with a side of beef tibs and injera'),
 ('Fish Combo', None, [], 'fried fish, fish tibs and salad with injera'),
 ('Doro Wot Mesob', None, ['spicy'], 'doro wot served in a woven mesob basket with injera'),
 ('Lunch Combo Rice and Wot', None, [], 'rice with key wot and salad'),
 ('Fasting Combo with Rice', None, ['fasting', 'vegetarian'], 'rice with shiro, misir and vegetables')]
for c in combo: ETH.append((c[0], c[1], 'combos', c[2], c[3]))

items = []
seen = set()
for name, am, cat, tags, desc in ETH + FAM:
    k = name.lower()
    if k in seen: continue
    seen.add(k)
    items.append({'name': name, 'name_am': am, 'category': cat, 'tags': tags, 'desc': desc})

# Fill to exactly 1,000 with further real menu variations, then trim.
extra_fill = []
for p in pizz[10:]: extra_fill.append((f'{p} Pizza Slice', 'pizza', [], 'single slice of {n} lifted with a cheese pull'))
for f in fresh: extra_fill.append((f'{f} Juice with Milk', 'juice', ['vegetarian'], 'tall glass of creamy {n}'))
for b in burg: extra_fill.append((f'{b} Burger Combo', 'burgers and sandwiches', [], '{n}: burger, fries and a soft drink'))
for s in ['Coca-Cola', 'Fanta Orange', 'Sprite', 'Mirinda', 'Pepsi', '7Up', 'Ambo Mineral Water', 'Still Water', 'Malt Drink', 'Energy Drink', 'Soda Water', 'Tonic Water', 'Ginger Ale', 'Apple Juice (Boxed)', 'Mango Juice (Boxed)']:
    extra_fill.append((s, 'soft drinks', ['fasting', 'vegetarian'], 'chilled bottle of {n} with condensation, glass with ice beside it'))
for g in grill: extra_fill.append((f'{g} with Rice', 'grill and meat', [], '{n}, plated with herbs'))
for p in pasta: extra_fill.append((f'{p} (Family Size)', 'pasta and rice', [], 'large family-size dish of {n}'))
for c in cakes: extra_fill.append((f'{c} (Whole)', 'cakes and pastries', ['vegetarian'], 'whole {n} on a cake stand'))
for s in soup: extra_fill.append((f'{s} (Large Bowl)', 'soups and salads', [], 'large bowl of {n}'))
for name, cat, tags, d in extra_fill:
    if len(items) >= 1000: break
    if name.lower() in seen: continue
    seen.add(name.lower())
    items.append({'name': name, 'name_am': None, 'category': cat, 'tags': tags, 'desc': d.format(n=name.lower())})
items = items[:1000]
assert len(items) == 1000, len(items)

# ---------- Add-on sets (beyond the 1,000): grid 41 = event catering buffet trays ----------
CATERING = [
 ('Key Wot Buffet Tray', ['spicy'], 'deep red berbere beef stew with tender beef chunks, glossy spiced-butter sheen'),
 ('Doro Wot Buffet Tray', ['spicy'], 'deep red berbere chicken stew with drumsticks and whole peeled boiled eggs'),
 ('Beef Tibs Buffet Tray', [], 'sautéed beef cubes with onion, rosemary and sliced green chili'),
 ('Lamb Tibs Buffet Tray', [], 'sautéed bone-in lamb pieces with onion, rosemary and green chili'),
 ('Siga Alicha Buffet Tray', [], 'mild golden turmeric beef stew with tender beef pieces'),
 ('Misir Wot Buffet Tray', ['fasting', 'vegetarian', 'spicy'], 'deep red spicy lentil stew topped with sliced green chili'),
 ('Shiro Buffet Tray', ['fasting', 'vegetarian'], 'smooth orange-brown chickpea shiro with a glossy oil sheen'),
 ('Kik Alicha Buffet Tray', ['fasting', 'vegetarian'], 'golden yellow split pea stew, smooth and mild'),
 ('Gomen Buffet Tray', ['fasting', 'vegetarian'], 'dark green braised collard greens with garlic and green chili'),
 ('Atkilt Wot Buffet Tray', ['fasting', 'vegetarian'], 'golden cabbage, carrot and potato stewed with turmeric'),
 ('Fasting Combo Buffet Tray', ['fasting', 'vegetarian'], 'divided chafing dish with misir wot, shiro, kik alicha and gomen side by side'),
 ('Dulet Buffet Tray', ['spicy'], 'finely chopped tripe, liver and lean beef with spiced butter, onion and green chili'),
 ('Kitfo Buffet Tray', [], 'minced lean beef in spiced butter and mitmita, with ayib and gomen in side sections'),
 ('Fried Fish Buffet Tray', ['fasting'], 'golden crispy fried fish pieces with lemon wedges'),
 ('Roast Chicken Buffet Tray', [], 'golden roast chicken pieces with crisp skin and herbs'),
 ('Beef Ribs Buffet Tray', [], 'glazed beef ribs, caramelised and glossy'),
 ('Meatballs in Sauce Buffet Tray', [], 'dark glossy beef meatballs in a rich sauce'),
 ('Rice Pilaf Buffet Tray', ['vegetarian'], 'fluffy spiced rice pilaf with carrot, peas and raisins'),
 ('Pasta in Tomato Sauce Buffet Tray', ['vegetarian'], 'penne in a rich red tomato sauce with herbs'),
 ('Roast Potatoes and Vegetables Buffet Tray', ['fasting', 'vegetarian'], 'golden roasted potatoes, carrots and green beans with rosemary'),
 ('Fresh Salad Buffet Bowl', ['fasting', 'vegetarian'], 'large bowl of fresh lettuce, tomato, cucumber, onion and green chili salad'),
 ('Injera Rolls Buffet Basket', ['fasting', 'vegetarian'], 'neatly rolled injera stacked in a woven basket on the buffet line'),
 ('Fruit Platter Buffet Display', ['fasting', 'vegetarian'], 'large platter of sliced mango, papaya, watermelon, pineapple and banana'),
 ('Mini Dessert Buffet Tray', ['vegetarian'], 'rows of mini pastries, cream cakes and fruit tarts'),
 ('Coffee Ceremony Buffet Station', ['vegetarian'], 'black clay jebena, small handleless cups on a tray, fresh grass and incense smoke'),
]
CATER_START = len(items)
for name, tags, d in CATERING:
    items.append({'name': name, 'name_am': None, 'category': 'catering', 'tags': tags, 'desc': d})
assert len(items) == 1025, len(items)

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
for i, it in enumerate(items):
    it['id'] = f'f{i + 1:04d}'
    it['slug'] = slug(it['name'])
    it['grid'] = i // 25 + 1
    it['cell'] = i % 25 + 1           # 1..25, left to right, top to bottom
    it['row'], it['col'] = (it['cell'] - 1) // 5 + 1, (it['cell'] - 1) % 5 + 1
    it['image'] = f"https://ageligil.cdn.et/foods/{it['slug']}.webp"
    it['review'] = 'native-check' if it['name_am'] or it['category'] in ('stews (wot)', 'fasting dishes', 'raw and minced meat', 'tibs', 'breakfast', 'bread', 'drinks (traditional)', 'combos') else 'ok'

HEAD = ("PHOTOGRAPHS ONLY. ABSOLUTELY NO TEXT ANYWHERE IN THE IMAGE: no dish names, no captions, no labels, no titles, "
 "no numbers, no letters, no logos, no watermarks, no menu cards, no signs. The dish names below are private reference "
 "for you; never write them in the image.")
STYLE = ("Ultra-realistic commercial food photography by a world-class food photographer. Each cell is a separate, complete "
 "studio-quality photo of ONE dish, shot at a natural 45-degree angle (top-down for flat platters and injera spreads), "
 "shallow depth of field, soft directional window light with gentle highlights and deep, rich shadows, appetising steam "
 "or condensation where it belongs, glossy sauces, crisp textures, true-to-life colours. Real Ethiopian serving ware "
 "where it fits: injera, black clay pots (shekla), woven mesob baskets, jebena coffee pots, small handleless cups; "
 "clean cafe crockery for cafe items. Warm, inviting, mouth-watering, magazine-cover quality.")
RULES = ("Layout: one square image (1:1) split into an exact 5x5 grid of 25 equal square photos, 5 rows of 5. "
 "Photos run edge to edge: no outer border, no frame, no margin. Between photos only a hairline-thin straight white line, "
 "as thin as possible, perfectly straight and evenly spaced. Every photo is the same size. "
 "Each photo shows exactly the dish given for its row and position, once, centred, filling about 75% of the photo. "
 "Every dish appears exactly once; never repeat a dish and never swap positions. No hands, no people, no cutlery clutter. "
 "Consistent lighting and colour grading across all 25 photos.")
CATER_STYLE = ("Ultra-realistic event-catering photography by a world-class food photographer, for a premium Ethiopian "
 "catering company. Each cell is a separate, complete photo of ONE generously filled rectangular buffet chafing dish with a "
 "polished gold rim and gold frame, on a buffet table dressed in crisp white linen, shot from a 45-degree angle looking down "
 "into the tray. Warm, elegant banquet-hall lighting with soft golden highlights on the metal, a gentle blurred row of more "
 "gold chafing dishes and soft drapery in the background, shallow depth of field, gentle steam rising, glossy sauces, rich "
 "true-to-life colours. Abundant, festive, wedding-reception quality, mouth-watering.")
TAIL = ("Final check: 25 distinct dishes in the order given, hairline white separators, no border, and zero text of any kind "
 "on or under any photo.")

os.makedirs('prompts', exist_ok=True)
ORD = ['first (left)', 'second', 'third (middle)', 'fourth', 'fifth (right)']
allp = []
GRID_STYLE = {41: CATER_STYLE}
NGRIDS = max(it['grid'] for it in items)
for g in range(1, NGRIDS + 1):
    cells = [it for it in items if it['grid'] == g]
    rows = []
    for r in range(1, 6):
        rc = [c for c in cells if c['row'] == r]
        rows.append(f"Row {r} (left to right):\n" + '\n'.join(f"- {ORD[c['col']-1]}: {c['desc']} [reference: {c['name']}]" for c in rc))
    p = f"{HEAD}\n\n{GRID_STYLE.get(g, STYLE)}\n\n{RULES}\n\n" + '\n\n'.join(rows) + f"\n\n{TAIL}\n"
    with open(f'prompts/grid-{g:02d}.md', 'w') as f:
        f.write(f"# Grid {g:02d} of {NGRIDS} (items {cells[0]['id']}–{cells[-1]['id']})\n\nAspect ratio 1:1, highest resolution available. Save the result as `grid-{g:02d}.png`.\n\n```\n{p}```\n")
    allp.append(f"## Grid {g:02d} ({cells[0]['id']}–{cells[-1]['id']}), save as grid-{g:02d}.png\n\n```\n{p}```\n")
with open('prompts/ALL.md', 'w') as f:
    f.write(f"# Ageligil food library: {NGRIDS} grid prompts ({len(items):,} dishes; grid 41 = catering trays)\n\nEach prompt makes one 1:1 image, a 5x5 grid. Cell n = item n of that grid in foods.json (grid, cell). "
            "Save each result as grid-NN.png in /Volumes/Vault/Ageligil/foods/grids; `node slice.mjs` cuts it into 25 photos named by slug.\n\n" + '\n'.join(allp))
with open('foods.json', 'w') as f:
    json.dump({'version': 1, 'count': len(items), 'note': 'Ethiopian names and Amharic spellings marked review: native-check need a native speaker.', 'items': items}, f, ensure_ascii=False, indent=1)
from collections import Counter
print(len(items), 'items;', Counter(i['category'] for i in items).most_common())
print('needs native check:', sum(1 for i in items if i['review'] == 'native-check'))
