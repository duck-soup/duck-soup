import random

def get_random_title(titles):
    emoji_list_food =  [    
        '🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬', '🥒', '🌶', '🌽', '🥕', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🥞', '🧀', '🍖', '🍗', '🥩', '🥓', '🍔', '🍟', '🍕', '🌭', '🥪', '🌮', '🌯', '🥙', '🥚', '🍳', '🥘', '🍲', '🥣', '🥗', '🍿', '🧂', '🥫', '🍱', '🍘', '🍙', '🍚', '🍛', '🍜', '🍝', '🍠', '🍢', '🍣', '🍤', '🍥', '🥮', '🍡', '🥟', '🥠', '🥡', '🦀', '🦞', '🦐', '🦑', '🍦', '🍧', '🍨', '🍩', '🍪', '🎂', '🍰', '🧁', '🥧', '🍫', '🍬', '🍭', '🍮', '🍯', '🍼', '🥛', '☕', '🍵', '🍶', '🍾', '🍷', '🍸', '🍹', '🍺']

    hundread_words_starting_with_A = [
        'Aardvark', 'Aardwolf', 'Albatross', 'Alligator', 'Alpaca', 'Ant', 'Anteater', 'Antelope', 'Ape', 'Armadillo', 'Donkey', 'Baboon', 'Badger', 'Barracuda', 'Bat', 'Bear', 'Beaver', 'Bee', 'Bison', 'Boar', 'Buffalo', 'Butterfly', 'Camel', 'Capybara', 'Caribou', 'Cassowary', 'Cat', 'Caterpillar', 'Cattle', 'Chamois', 'Cheetah', 'Chicken', 'Chimpanzee', 'Chinchilla', 'Chough', 'Clam', 'Cobra', 'Cockroach', 'Cod', 'Cormorant', 'Coyote', 'Crab', 'Crane', 'Crocodile', 'Crow', 'Curlew', 'Deer', 'Dinosaur', 'Dog', 'Dogfish', 'Dolphin', 'Dotterel', 'Dove', 'Dragonfly', 'Duck', 'Dugong', 'Dunlin', 'Eagle', 'Echidna', 'Eel', 'Eland', 'Elephant', 'Elephant Seal', 'Elk', 'Emu', 'Falcon', 'Ferret', 'Finch', 'Fish', 'Flamingo', 'Fly', 'Fox', 'Frog', 'Gaur', 'Gazelle', 'Gerbil', 'Giant Panda', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfinch', 'Goldfish', 'Goose', 'Gorilla', 'Goshawk', 'Grasshopper', 'Grouse', 'Guanaco', 'Gull', 'Hamster', 'Hare', 'Hawk', 'Hedgehog', 'Heron', 'Herring', 'Hippopotamus', 'Hornet', 'Horse', 'Human', 'Hummingbird', 'Hyena', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Kangaroo', 'Kingfisher', 'Koala', 'Komodo Dragon', 'Kouprey', 'Kudu', 'Lapwing'
    ]

    hundread_words_starting_with_C = [
        'Cockroach', 'Cod', 'Cormorant', 'Coyote', 'Crab', 'Crane', 'Crocodile', 'Crow', 'Curlew', 'Deer', 'Dinosaur', 'Dog', 'Dogfish', 'Dolphin', 'Dotterel', 'Dove', 'Dragonfly', 'Duck', 'Dugong', 'Dunlin', 'Eagle', 'Echidna', 'Eel', 'Eland', 'Elephant', 'Elephant Seal', 'Elk', 'Emu', 'Falcon', 'Ferret', 'Finch', 'Fish', 'Flamingo', 'Fly', 'Fox', 'Frog', 'Gaur', 'Gazelle', 'Gerbil', 'Giant Panda', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfinch', 'Goldfish', 'Goose', 'Gorilla', 'Goshawk', 'Grasshopper', 'Grouse', 'Guanaco', 'Gull', 'Hamster', 'Hare', 'Hawk', 'Hedgehog', 'Heron', 'Herring', 'Hippopotamus', 'Hornet', 'Horse', 'Human', 'Hummingbird', 'Hyena', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Kangaroo', 'Kingfisher', 'Koala', 'Komodo Dragon', 'Kouprey', 'Kudu', 'Lapwing', 'Lark', 'Lemur', 'Leopard', 'Lion', 'Llama', 'Lobster', 'Locust', 'Loris', 'Louse', 'Lyrebird', 'Magpie', 'Mallard', 'Manatee', 'Mandrill', 'Mantis', 'Marten', 'Meerkat', 'Mink', 'Mole', 'Mongoose', 'Monkey', 'Moose', 'Mosquito', 'Mouse', 'Mule', 'Narwhal', 'Newt', 'Nightingale', 'Octopus', 'Okapi', 'Opossum', 'Oryx', 'Ostrich', 'Otter', 'Owl', 'Oyster', 'Panther', 'Parrot'

    ]
    hundread_words_starting_with_D = [
        'Deer', 'Dinosaur', 'Dog', 'Dogfish', 'Dolphin', 'Dotterel', 'Dove', 'Dragonfly', 'Duck', 'Dugong', 'Dunlin', 'Eagle', 'Echidna', 'Eel', 'Eland', 'Elephant', 'Elephant Seal', 'Elk', 'Emu', 'Falcon', 'Ferret', 'Finch', 'Fish', 'Flamingo', 'Fly', 'Fox', 'Frog', 'Gaur', 'Gazelle', 'Gerbil', 'Giant Panda', 'Giraffe', 'Gnat', 'Gnu', 'Goat', 'Goldfinch', 'Goldfish', 'Goose', 'Gorilla', 'Goshawk', 'Grasshopper', 'Grouse', 'Guanaco', 'Gull', 'Hamster', 'Hare', 'Hawk', 'Hedgehog', 'Heron', 'Herring', 'Hippopotamus', 'Hornet', 'Horse', 'Human', 'Hummingbird', 'Hyena', 'Jackal', 'Jaguar', 'Jay', 'Jellyfish', 'Kangaroo', 'Kingfisher', 'Koala', 'Komodo Dragon', 'Kouprey', 'Kudu', 'Lapwing', 'Lark', 'Lemur', 'Leopard', 'Lion', 'Llama', 'Lobster', 'Locust', 'Loris', 'Louse', 'Lyrebird', 'Magpie', 'Mallard', 'Manatee', 'Mandrill', 'Mantis', 'Marten', 'Meerkat', 'Mink', 'Mole', 'Mongoose', 'Monkey', 'Moose', 'Mosquito', 'Mouse', 'Mule', 'Narwhal', 'Newt', 'Nightingale', 'Octopus', 'Okapi', 'Opossum', 'Oryx', 'Ostrich', 'Otter', 'Owl', 'Oyster', 'Panther', 'Parrot', 'Parrotfish', 'Partridge', 'Peafowl', 'Pelican', 'Penguin', 'Pheasant', 'Pig', 'Pigeon', 'Pony',

    ]
    while True:
        random_emoji = random.choice(emoji_list_food)         
        random_title = random.choice(hundread_words_starting_with_C) + ' ' + random.choice(hundread_words_starting_with_D) + ' ' +  random.choice(hundread_words_starting_with_A)
        if random_title not in titles:
            titles.append(random_title)
            break
    # check unicity
    return random_emoji, random_title

css_table_ = '''
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            border-radius: 5px;
        }
        th, td {
            border-radius: 5px;
            text-align: left;
            padding: 8px;
        }
        tr:nth-child(even){background-color: #f2f2f2}
        th {
            background-color: #2196F3;
            color: white;
        }
        table {
            -webkit-user-drag: element;
            -webkit-user-modify: read-write-plaintext-only;
            -webkit-touch-callout: none;
            -webkit-tap-highlight-color: rgba(0,0,0,0);
        }
        input[type=checkbox] {
            transform: scale(1.5);
        }
    </style>
'''
css_table = '''
 <style>
    table {
        border-collapse: collapse;
        border-radius: 5px;
        position: absolute;
    }
    th, td {
        border-radius: 5px;
        text-align: left;
        padding: 8px;
    }
    tr:nth-child(even){background-color: #f2f2f2}
    th {
        background-color: #2196F3;
        color: white;
    }
    table {
        -webkit-user-drag: element;
        -webkit-user-modify: read-write-plaintext-only;
        -webkit-touch-callout: none;
        -webkit-tap-highlight-color: rgba(0,0,0,0);
    }
    input[type=checkbox] {
        transform: scale(1.5);
    }
    .resize-handle {
        width: 10px;
        height: 10px;
        background-color: white;
        border: 1px solid black;
        position: absolute;
        z-index: 999;
    }
</style>
<script>
    // This is a JavaScript script that will be executed when the webview has finished loading
    // You can interact with the webview here
    let table = document.querySelector('table');
    let isDragging = false;
    let startX, startY, startWidth, startHeight;
    let isResizing = false;
    let minWidth = 50;
    let minHeight = 50;

    // Add a double-click event listener to the table to capture the starting position of the mouse
    table.addEventListener('dblclick', (event) => {
        if (!isResizing) {
            table.style.position = 'absolute';
            startX = event.clientX - table.offsetLeft;
            startY = event.clientY - table.offsetTop;
            isDragging = true;
        }
    });

    // Add a mousemove event listener to the document to move the table while the mouse is moved
    document.addEventListener('mousemove', (event) => {
        if (isDragging) {
            table.style.left = event.clientX - startX + 'px';
            table.style.top = event.clientY - startY + 'px';
        }
    });

    // Add a mouseup event listener to the document to stop the dragging by removing the mousemove event listener
    document.addEventListener('mouseup', (event) => {
        isDragging = false;
    });

    // Add a mousedown event listener to the corner of the table to capture the starting position of the mouse
    let corner = document.createElement('div');
    corner.style.position = 'absolute';
    corner.style.width = '10px';
    corner.style.height = '10px';
    corner.style.bottom = '0';
    corner.style.right = '0';
    corner.style.cursor = 'se-resize';
    table.appendChild(corner);

    corner.addEventListener('mousedown', (event) => {
        isResizing = true;
        startX = event.clientX;
        startY = event.clientY;
        startWidth = parseInt(document.defaultView.getComputedStyle(table).width, 10);
        startHeight = parseInt(document.defaultView.getComputedStyle(table).height, 10);
    });

    // Add a mousemove event listener to the document to resize the table while the mouse is moved
    document.addEventListener('mousemove', (event) => {
        if (isResizing) {
            let width = startWidth + (event.clientX - startX);
            let height = startHeight + (event.clientY - startY);
            width = Math.max(width, minWidth);
            height = Math.max(height, minHeight);
            table.style.width = width + 'px';
            table.style.height = height + 'px';
        }
    });

    // Add a mouseup event listener to the document to stop the resizing by removing the mousemove event listener
    document.addEventListener('mouseup', (event) => {
        isResizing = false;
    });
</script>
'''

