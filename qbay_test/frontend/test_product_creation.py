import os
from seleniumbase import BaseCase
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.models import User
from qbay.users import register, login
from qbay.products import create_product

"""
This file defines all integration tests for the frontend product creation.
"""


class FrontEndProductCreationPage(BaseCase):
    def test_product_creation_r4_1(self, *_):
        """
        Testing R4-1: The title of the product has to be alphanumeric-only,
        and space allowed only if it is not as prefix and suffix.

        Input Coverage: Covers a P1: valid title, P2: invalid title (not
                        alphanumeric and spaces only), P3: invalid title
                        (space as prefix), and P4: invalid title (space as
                        suffix).
        Output Coverage: Covers P1: valid title, and P2: invalid title.
        """
        assert register('Vert Wheeler', 'acceleracers@hotwheels.com',
                        'SeQure12#34') is True
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Input & Output Testing - Title
        # P1: valid title. Tests both Input P1 & Output P1.
        self.open(base_url + "/product-creation")
        self.type("#product-name", "Banana Pie")
        self.type("#description", "A hot and fresh banana pie, buy now!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")  # Success

        # P2: invalid title (title not a combination of alphanumerics and
        #     spaces). Tests both Input P2 & Output P2.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Tongue-Twister")
        self.type("#description", "Like the game twister but with words!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P3: invalid title (title has space at the beginning)
        self.open(base_url + '/product-creation')
        self.type("#product-name", " Bean Bag Chair")
        self.type("#description", "A really cushy chair to sit in and relax!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P4: invalid title (title has space at the end)
        self.open(base_url + '/product-creation')
        self.type("#product-name", "IKEA Table ")
        self.type("#description", "What more is there to say?")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

    def test_product_creation_r4_2(self, *_):
        """
        Testing R4-2: The title of the product is no longer than 80
                      characters.

        Input Coverage: Covers a P1: valid title (under 80 characters), and
                        P2: invalid title (over 80 characters).
        Output Coverage: Covers P1: valid title, and P2: invalid title.
        """
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Input & Output Testing - Title
        # P1: valid title (under 80 characters). Tests both Input P1 & Output
        #     P1.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Flatscreen TV")
        self.type("#description", "A 38-inch flatscreen tv!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P2: invalid title (over 80 characters). Tests both Input P2 & Output
        #     P2.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "supercalifragilisticexpialidocious" +
                                   "supercalifragilisticexpialidocious" +
                                   "supercalifragilisticexpialidocious")
        self.type("#description", "ADJECTIVE: supercalifragilistic " +
                                  "(adjective)\n" +
                                  "Meaning: extraordinarily good; " +
                                  "wonderful.\n" +
                                  "Example: the only word to " +
                                  "characterize Kepler's discoveries was " +
                                  "‘Supercalifragilisticexpialidocious’")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

    def test_product_creation_r4_3(self, *_):
        """
        Testing R4-3: The description of the product can be arbitrary
                      characters, with a minimum length of 20 characters and a
                      maximum of 2000 characters.

        Input Coverage: Covers a P1: valid description (between 20 and 2000
                        characters inclusive), P2: invalid description (less
                        than 20 characters), and P3: invalid description (more
                        than 2000 characters).
        Output Coverage: Covers P1: valid description, and P2: invalid
                         description.
        """
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Input & Output Testing - Description
        # P1: valid description (between 20 and 2000 characters inclusive).
        #     Tests both Input P1 & Output P1.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Super Mario Bros")
        self.type("#description", "The very first Super Mario game for the " +
                                  "NES!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P2: invalid description (less than 20 characters). Tests both Input
        #     P2 & Output P2.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "SMB3")
        self.type("#description", "Third mario game")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P3: invalid description (more than 2000 characters).
        self.open(base_url + '/product-creation')
        self.type("#product-name", "SMB2")
        self.type("#description", "Super Mario Bros. 2 is a platform video " +
                                  "game developed and published by " +
                                  "Nintendo for the Nintendo Entertainment " +
                                  "System. The game was first released in " +
                                  "North America in October 1988, and in " +
                                  "the PAL region the following year. It " +
                                  "has been remade or re-released for " +
                                  "several video game consoles. The " +
                                  "Western release of Super Mario Bros. 2 " +
                                  "was based on Yume Kōjō: Doki Doki " +
                                  "Panic, a Family Computer Disk System " +
                                  "game meant to tie-in with Fuji " +
                                  "Television's media technology expo, " +
                                  "called Yume Kōjō (lit. Dream Factory). " +
                                  "The characters, enemies, and themes of " +
                                  "the game were meant to reflect the " +
                                  "mascots and theme of the festival. After" +
                                  " Nintendo of America found the Japanese " +
                                  "version of Super Mario Bros. 2 (later " +
                                  "released internationally as Super Mario " +
                                  "Bros.: The Lost Levels) to be too " +
                                  "difficult and similar to its " +
                                  "predecessor, Yume Kōjō: Doki Doki Panic " +
                                  "was modified to become Super Mario " +
                                  "Bros. 2 for release outside of Japan. A " +
                                  "commercial success, the international " +
                                  "Super Mario Bros. 2 was re-released in " +
                                  "Japan for the Famicom as Super Mario " +
                                  "USA (1992), as part of the Super Mario " +
                                  "All-Stars (1993) collection for the " +
                                  "Super NES (including the Japanese Super " +
                                  "Mario Bros. 2 as The Lost Levels), and " +
                                  "as Super Mario Advance (2001) for the " +
                                  "Game Boy Advance. Gameplay: Super Mario " +
                                  "Bros. 2 is a 2D side-scrolling platform " +
                                  "game. The objective of the game is to " +
                                  "navigate the player's character through " +
                                  "the dream world Subcon and defeat the " +
                                  "main antagonist Wart. Before each " +
                                  "stage, the player chooses one of four " +
                                  "different protagonists to use: Mario, " +
                                  "Luigi, Toad, and Princess Toadstool. " +
                                  "Unlike the previous game, this game " +
                                  "does not have multiplayer functionality. " +
                                  "There is also no time limit to complete " +
                                  "any level. All four characters can run, " +
                                  "jump, and climb ladders or vines, but " +
                                  "each character possesses a unique " +
                                  "strength that causes them to be " +
                                  "controlled differently. For example, " +
                                  "Luigi can jump the highest; Princess " +
                                  "Toadstool can float; Toad's strength " +
                                  "allows him to pick up items quickly; " +
                                  "and Mario represents the best balance " +
                                  "between jumping and strength. As " +
                                  "opposed to the original Super Mario " +
                                  "Bros., which only moved from left to " +
                                  "right, players can move either left or " +
                                  "right, as well as vertically in " +
                                  "waterfall, cloud and cave levels.")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

    def test_product_creation_r4_4(self, *_):
        """
        Testing R4-4: Description has to be longer than the product's title.

        Input Coverage: Covers a P1: valid title & description
                        (description is longer than title), and P2: invalid
                        title and description (description is shorter than
                        title).
        Output Coverage: Covers P1: valid title & description, and P2: invalid
                         title & description.
        """
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Input & Output Testing - Title & Description
        # P1: valid title & description (description is longer than title).
        #     Tests both Input P1 & Output P1.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "The Legend of Zelda")
        self.type("#description", "The original LoZ game for the NES!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P2: invalid title & description (description is shorter than title).
        #     Tests both Input P2 & Output P2.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "The Legend of Zelda A Link to the Past")
        self.type("#description", "A popular LoZ game for the GBA!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

    def test_product_creation_r4_5(self, *_):
        """
        Testing R4-5: Price has to be of range [10, 10000].

        Input Coverage: Covers a P1: valid price (price between 10 & 10000
                        inclusive), P2: invalid price (price less than 10),
                        and P3: invalid price (price greater than 10000).
        Output Coverage: Covers P1: valid price, and P2: invalid price.
        """
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Input & Output Testing - Price
        # P1: valid price (price between 10 & 10000 inclusive).
        #     Tests both Input P1 & Output P1.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "The Legend of Zelda Reg")
        self.type("#description", "A regular copy of the original LoZ game " +
                                  "for the NES.")
        self.type("#price", "50")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P2: invalid price (price less than 10).
        #     Tests both Input P2 & Output P2.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "The Legend of Zelda Cereal")
        self.type("#description", "Cereal themed after the famous LoZ games!")
        self.type("#price", "9")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P3: invalid price (price greater than 10000).
        self.open(base_url + '/product-creation')
        self.type("#product-name", "The Legend of Zelda Mint")
        self.type("#description", "A mint condition copy of the original " +
                                  "LoZ game for the NES!")
        self.type("#price", "10001")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

    def test_product_creation_r4_7(self, *_):
        """
        Testing R4-7: owner_email cannot be empty. The owner of the
                      corresponding product must exist in the database.

        Input Coverage: Covers a P1: valid user (user in database), and
                        P2: invalid user (user not in database).
        Output Coverage: Covers P1: valid user, and P2: invalid user.
        """

        # Input & Output Testing - User
        # P1: valid user (user in database).
        #     Tests both Input P1 & Output P1.
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Attempt to create a product with the user logged in
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Hot Wheels Car")
        self.type("#description", "A classic toy Hot Wheels car!")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P2: invalid user (user not in database).
        #     Tests both Input P2 & Output P2.
        # Attempt to log in with a user not in the database.
        self.open(base_url + "/login")
        self.type("#email", "callum@gmail.com")
        self.type("#password", "Password#1234")
        self.click('input[type="submit"]')
        self.assert_text("login failed", "#message")

    def test_product_creation_r4_8(self, *_):
        """
        Testing R4-8: A user cannot create products that have the same title.

        Input Coverage: Covers a P1: valid title (unique title), and
                        P2: invalid title (title already in database).
        Output Coverage: Covers P1: valid title, and P2: invalid title.
        """
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Input & Output Testing - Title
        # P1: valid title (unique title).
        #     Tests both Input P1 & Output P1.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Ferrari")
        self.type("#description", "A very stylish sports car.")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P2: invalid title (title already in database).
        #     Tests both Input P2 & Output P2.
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Ferrari")
        self.type("#description", "The same very stylish sports car.")
        self.type("#price", "10")
        self.type("#quantity", "1")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

    def test_product_creation_r4_8(self, *_):
        """
        Testing all requirements.

        Shotgun testing (of input): Testing various random inputs as detailed
                                    below.
        """
        self.open(base_url + "/login")
        self.type("#email", "acceleracers@hotwheels.com")
        self.type("#password", "SeQure12#34")
        self.click('input[type="submit"]')
        self.assert_title("Profile")  # Success!

        # Shotgun Testing
        # P1: invalid title
        self.open(base_url + '/product-creation')
        self.type("#product-name", "LG 50UM6951 50 4K UHD Smart LED TV, " +
                                   "Black")
        self.type("#description", "4K Ultra HD (3,840 x 2,160p) resolution " +
                                  "with TruMotion 120 offers pristine " +
                                  "detail and is clear in every moment. " +
                                  "Fast, accurate quad-core processing " +
                                  "eliminates noise and up-scales lower " +
                                  "resolution content to near 4K quality.")
        self.type("#price", "550")
        self.type("#quantity", "11")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P2: valid product
        self.open(base_url + '/product-creation')
        self.type("#product-name", "LEGO City Advent Calendar 60303 " +
                                   "Building Kit")
        self.type("#description", "Kids aged 5 and up can enjoy " +
                                  "imaginative play each December day with " +
                                  "this LEGO City Advent Calendar (60303) " +
                                  "– bursting with awesome mini-builds, " +
                                  "fun LEGO City TV characters and cool " +
                                  "accessories.")
        self.type("#price", "38")
        self.type("#quantity", "120")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P3: invalid title & price
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Oral-B Complete SatinFloss Dental Floss")
        self.type("#description", "Includes two 50 M packs of Oral-B " +
                                  "Complete SatinFloss Dental Floss.")
        self.type("#price", "5")
        self.type("#quantity", "365")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P4: invalid title & description
        self.open(base_url + '/product-creation')
        self.type("#product-name", "The Creature from Jekyll Island: A " +
                                   "Second Look at the Federal Reserve")
        self.type("#description", "Where does money come from?")
        self.type("#price", "30")
        self.type("#quantity", "15")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P5: valid product
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Klara and the Sun Hardcover")
        self.type("#description", "\"Moving & beautiful... an unequivocal " +
                                  "return to form.\" -Los Angeles Times")
        self.type("#price", "35")
        self.type("#quantity", "132")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P6: valid product
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Fitbit Versa 3 Health and Fitness " +
                                   "Smartwatch with GPS")
        self.type("#description", "Run, bike, hike and more phone-free—and " +
                                  "see your real-time pace & distance—with " +
                                  "built-in GPS. Then check out your " +
                                  "workout intensity map in the Fitbit app.")
        self.type("#price", "199")
        self.type("#quantity", "4")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")

        # P7: invalid title & description
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Garmin Venu Sq Music, GPS Smartwatch " +
                                   "with Bright Touchscreen Display, " +
                                   "Features Music and Up to 6 Days of " +
                                   "Battery Life, White and Slate")
        self.type("#description", "Fits wrists with a circumference of " +
                                  "125-190 mm. See everything clearly on a " +
                                  "bright color display that includes an " +
                                  "always-on mode, perfect for quick " +
                                  "glances. Health is important to you, so " +
                                  "monitor everything from your Body " +
                                  "Battery energy levels, respiration, " +
                                  "hydration and stress to sleep, your " +
                                  "menstrual cycle, estimated heart rate " +
                                  "and more.")
        self.type("#price", "199")
        self.type("#quantity", "4")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P8: invalid title, description, & price
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Crosshairs: A Novel")
        self.type("#description", "Book")
        self.type("#price", "0")
        self.type("#quantity", "0")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P9: invalid price
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Colgate Sensitive Pro Relief Repair " +
                                   "and Prevent Toothpaste")
        self.type("#description", "Helps stop sensitivity pain at the " +
                                  "source when used as directed.")
        self.type("#price", "7")
        self.type("#quantity", "25")
        self.click('input[type="submit"]')
        self.assert_text("Product creation failed.", "#message")

        # P10: valid product
        self.open(base_url + '/product-creation')
        self.type("#product-name", "Toms of Maine Northwoods Long Lasting " +
                                   "Natural Deodorant")
        self.type("#description", "Aluminum-free: feel fresh all day with " +
                                  "a bespoke blend of all natural " +
                                  "ingredients that provide 24-hour odor " +
                                  "protection.")
        self.type("#price", "10")
        self.type("#quantity", "3200")
        self.click('input[type="submit"]')
        self.assert_text("Welcome Vert Wheeler!", "#welcome-header")
