# Product Creation Testing Design

The tables below are used to partition testing into various cases based on the requirements given for the code. All of the below testing is _black box testing_, and is separated by each requirement. Each requirement has tests for input partioning, output partitioning, and **TODO**. Most output partitioning is covered by the input partitioning tests (the tests are not repeated during system testing, but understood to cover all output partitions).

## Testing R4-1:

The title of the product has to be alphanumeric-only, and space allowed only if it is not as prefix and suffix. For these examples, a "\_" character is considered a space for titles only (used for clarity).

**Input Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title) | Banana*Pie | A hot and fresh banana pie, buy now! | 10 | 1
P2 (invalid title - not alphanumeric & spaces only) | Tongue-Twister | Like the game twister but with words! | 10 | 1
P3 (invalid title - space as prefix) | \_Bean_Bag_Chair | A really cushy chair to sit in and relax! | 10 | 1
P4 (invalid title - space as suffix) | IKEA_Table* | What more is there to say? | 10 | 1

**Output Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title) | Banana_Pie | A hot and fresh banana pie, buy now! | 10 | 1
P2 (invalid title - not alphanumeric & spaces only) | Tongue-Twister | Like the game twister but with words! | 10 | 1

---

## Testing R4-2:

The title of the product is no longer than 80 characters.

**Input Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title - under 80 characters) | Flatscreen_TV | A 38-inch flatscreen tv! | 10 | 1
P2 (invalid title - over 80 characters) | supercalifragilisticexpialidocioussupercalifragilisticexpialidocioussupercalifragilisticexpialidocious | ADJECTIVE: supercalifragilistic (adjective). Meaning: extraordinarily good; wonderful. Example: the only word to characterize Kepler's discoveries was ‘Supercalifragilisticexpialidocious’ | 10 | 1

**Output Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title - under 80 characters) | Flatscreen_TV | A 38-inch flatscreen tv! | 10 | 1
P2 (invalid title - over 80 characters) | supercalifragilisticexpialidocioussupercalifragilisticexpialidocioussupercalifragilisticexpialidocious | ADJECTIVE: supercalifragilistic (adjective). Meaning: extraordinarily good; wonderful. Example: the only word to characterize Kepler's discoveries was ‘Supercalifragilisticexpialidocious’ | 10 | 1

---

## Testing R4-3:

The description of the product can be arbitrary characters, with a minimum length of 20 characters and a maximum of 2000 characters.

**Input Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid description - between 20 and 2000 characters inclusive) | Super_Mario_Bros | The very first Super Mario game for the NES! | 10 | 1
P2 (invalid description - less than 20 characters) | SMB3 | Third mario game | 10 | 1
P3 (invalid description - more than 2000 characters) | SMB2 | Super Mario Bros. 2 is a platform video game developed and published by Nintendo for the Nintendo Entertainment System. The game was first released in North America in October 1988, and in the PAL region the following year. It has been remade or re-released for several video game consoles. The Western release of Super Mario Bros. 2 was based on Yume Kōjō: Doki Doki Panic, a Family Computer Disk System game meant to tie-in with Fuji Television's media technology expo, called Yume Kōjō (lit. Dream Factory). The characters, enemies, and themes of the game were meant to reflect the mascots and theme of the festival. After Nintendo of America found the Japanese version of Super Mario Bros. 2 (later released internationally as Super Mario Bros.: The Lost Levels) to be too difficult and similar to its predecessor, Yume Kōjō: Doki Doki Panic was modified to become Super Mario Bros. 2 for release outside of Japan. A commercial success, the international Super Mario Bros. 2 was re-released in Japan for the Famicom as Super Mario USA (1992), as part of the Super Mario All-Stars (1993) collection for the Super NES (including the Japanese Super Mario Bros. 2 as The Lost Levels), and as Super Mario Advance (2001) for the Game Boy Advance. Gameplay: Super Mario Bros. 2 is a 2D side-scrolling platform game. The objective of the game is to navigate the player's character through the dream world Subcon and defeat the main antagonist Wart. Before each stage, the player chooses one of four different protagonists to use: Mario, Luigi, Toad, and Princess Toadstool. Unlike the previous game, this game does not have multiplayer functionality. There is also no time limit to complete any level. All four characters can run, jump, and climb ladders or vines, but each character possesses a unique strength that causes them to be controlled differently. For example, Luigi can jump the highest; Princess Toadstool can float; Toad's strength allows him to pick up items quickly; and Mario represents the best balance between jumping and strength. As opposed to the original Super Mario Bros., which only moved from left to right, players can move either left or right, as well as vertically in waterfall, cloud and cave levels. | 10 | 1

**Output Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid description - between 20 and 2000 characters inclusive) | Super_Mario_Bros | The very first Super Mario game for the NES! | 10 | 1
P2 (invalid description - less than 20 characters) | SMB3 | Third mario game | 10 | 1

---

## Testing R4-4:

Description has to be longer than the product's title.

**Input Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title & description - description is longer than title) | The_Legend_of_Zelda | The original LoZ game for the NES! | 10 | 1
P2 (invalid title & description - description is shorter than title) | The_Legend_of_Zelda_A_Link_to_the_Past | A popular LoZ game for the GBA! | 10 | 1

**Output Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title & description - description is longer than title) | The_Legend_of_Zelda | The original LoZ game for the NES! | 10 | 1
P2 (invalid title & description - description is shorter than title) | The_Legend_of_Zelda_A_Link_to_the_Past | A popular LoZ game for the GBA! | 10 | 1

---

## Testing R4-5:

Price has to be of range [10, 10000].

**Input Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid price - price is between 10 and 10000 inclusive) | The_Legend_of_Zelda_Reg | A regular copy of the original LoZ game for the NES. | 50 | 1
P2 (invalid price - price is less than 10) | The_Legend_of_Zelda_Cereal | Cereal themed after the famous LoZ games! | 9 | 1
P3 (invalid price - price is more than 10000) | The_Legend_of_Zelda_Mint | A mint condition copy of the original LoZ game for the NES! | 10001 | 1

**Output Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid price - price is between 10 and 10000 inclusive) | The_Legend_of_Zelda_Mint | A mint condition copy of the original LoZ game for the NES! | 10 | 1
P2 (invalid price - price is less than 10) | The_Legend_of_Zelda_Cereal | Cereal themed after the famous LoZ games! | 9 | 1

---

## Testing R4-6:

last_modified_date must be after 2021-01-02 and before 2025-01-02.

**Input Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid date - product was created between 2021-01-02 and before 2025-01-02 exclusive) | An_IKEA_Bed | A DIY style bed from IKEA! | 10 | 1
P2 (invalid date - product was created before 2021-01-02) | An_IKEA_Chair | A DIY style chair from IKEA! | 10 | 1
P3 (invalid date - product was created after 2025-01-02) | An_IKEA_Bookshelf | A DIY style bookshelf from IKEA! | 10 | 1

**Output Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid date - product was created between 2021-01-02 and before 2025-01-02 exclusive) | An_IKEA_Bed | A DIY style bed from IKEA! | 10 | 1
P2 (invalid date - product was created before 2021-01-02) | An_IKEA_Chair | A DIY style chair from IKEA! | 10 | 1

---

## Testing R4-7:

owner_email cannot be empty. The owner of the corresponding product must exist in the database.

**Input Partitioning:**
Partition | User Email | User Password | User in Database? | Product Name | Description | Price ($) | Quantity
----------|------------|---------------|-------------------|--------------|-------------|-----------|---------
P1 (valid user - user in database) | acceleracers@hotwheels.com | SeQure12#34 | Yes | Hot_Wheels_Car | A classic toy Hot Wheels car! | 10 | 1
P2 (invalid user - user not in database) | callum@gmail.com | Password#1234 | No | Garmin_Watch | A Garming GPS running watch. | 10 | 1

**Output Partitioning:**
Partition | User Email | User Password | User in Database? | Product Name | Description | Price ($) | Quantity
----------|------------|---------------|-------------------|--------------|-------------|-----------|---------
P1 (valid user - user in database) | acceleracers@hotwheels.com | SeQure12#34 | Yes | Hot_Wheels_Car | A classic toy Hot Wheels car! | 10 | 1
P2 (invalid user - user not in database) | callum@gmail.com | Password#1234 | No | Garmin_Watch | A Garming GPS running watch. | 10 | 1

---

## Testing R4-8:

A user cannot create products that have the same title.

**Input Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title - unique title) | Ferrari | A very stylish sports car. | 10 | 1
P2 (invalid title - title already used by other product) | Ferrari | The same very stylish sports car. | 10 | 1

**Output Partitioning:**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (valid title - unique title) | Ferrari | A very stylish sports car. | 10 | 1
P2 (invalid title - title already used by other product) | Ferrari | The same very stylish sports car. | 10 | 1

---

## Testing of all Requirements

Various tests randomly generated for shotgun testing (covers a variety of product requirements).

**Shotgun Testing**
Partition | Product Name | Description | Price ($) | Quantity
----------|--------------|-------------|-----------|---------
P1 (invalid title) | LG 50UM6951 50 4K UHD Smart LED TV, Black | 4K Ultra HD (3,840 x 2,160p) resolution with TruMotion 120 offers pristine detail and is clear in every moment. Fast, accurate quad-core processing eliminates noise and up-scales lower resolution content to near 4K quality. | 550 | 11
P2 (valid product) | LEGO City Advent Calendar 60303 Building Kit | Kids aged 5 and up can enjoy imaginative play each December day with this LEGO City Advent Calendar (60303) – bursting with awesome mini-builds, fun LEGO City TV characters and cool accessories. | 38 | 120
P3 (invalid title & price) | Oral-B Complete SatinFloss Dental Floss | Includes two 50 M packs of Oral-B Complete SatinFloss Dental Floss. | 5 | 365
P4 (invalid title & description) | The Creature from Jekyll Island: A Second Look at the Federal Reserve | Where does money come from? | 30 | 15
P5 (valid product) | Klara and the Sun Hardcover | "Moving & beautiful... an unequivocal return to form." -Los Angeles Times | 35 | 132
P6 (valid product) | Fitbit Versa 3 Health and Fitness Smartwatch with GPS | Run, bike, hike and more phone-free—and see your real-time pace & distance—with built-in GPS. Then check out your workout intensity map in the Fitbit app. | 199 | 4
P7 (invalid title) | Garmin Venu Sq Music, GPS Smartwatch with Bright Touchscreen Display, Features Music and Up to 6 Days of Battery Life, White and Slate | Fits wrists with a circumference of 125-190 mm. See everything clearly on a bright color display that includes an always-on mode, perfect for quick glances. Health is important to you, so monitor everything from your Body Battery energy levels, respiration, hydration and stress to sleep, your menstrual cycle, estimated heart rate and more. | 199 | 4
P8 (invalid title, description, and price) | Crosshairs: A Novel | Book | 0 | 0
P9 (invalid price) | Colgate Sensitive Pro Relief Repair and Prevent Toothpaste | Helps stop sensitivity pain at the source when used as directed. | 7 | 25
P10 (valid product) | Toms of Maine Northwoods Long Lasting Natural Deodorant | Aluminum-free: feel fresh all day with a bespoke blend of all natural ingredients that provide 24-hour odor protection. | 10 | 3200
