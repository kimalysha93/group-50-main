from seleniumbase import BaseCase

from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.users import register
from qbay.products import create_product


class FrontEndUpdateProductPage(BaseCase):
    """
    R5-1: One can update all attributes of the product, except owner_email
          and last_modified_date.
    """

    def test_update_product_r5_4_title(self, *_):
        """
        R5-4: When updating an attribute, one has to make sure that it follows
              the same requirements as above.

        R4-1: The title of the product has to be alphanumeric-only, and space
              allowed only if it is not as prefix and suffix.

        R4-2: The title of the product is no longer than 80 characters.

        R4-4: Description has to be longer than the product's title.
        """

        # Create a test user and some teset products, and login with that user
        assert register('KWW', 'gggg@queensu.com', 'GrEgOrY1!') is True
        assert create_product('Nintendo Wii',
                              'Play games on this console such as Mario',
                              20000, 'gggg@queensu.com') is True
        assert create_product('Baked beans', 'They taste pretty good',
                              1000, 'gggg@queensu.com') is True
        self.open(base_url + '/login')
        self.type('#email', 'gggg@queensu.com')
        self.type('#password', 'GrEgOrY1!')
        self.click('input[type="submit"]')
        self.assert_title('Profile')

        # Input coverage:
        # (VALID) Update product title (valid length and is not longer than
        # the description)
        self.click('input[name="Nintendo Wii"]')
        self.assert_title('Update a Product')
        self.type('#product-name', 'Nintendo Gamecube')
        self.click('input[type="submit"]')
        self.assert_title('Profile')
        self.assert_text('Welcome KWW!', '#welcome-header')

        # (INVALID) Update product title (valid length but is longer
        # than the description)
        self.click('input[name="Nintendo Gamecube"]')
        self.assert_title('Update a Product')
        self.type('#product-name',
                  'Check out this cool and new console, never seen before!')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # (INVALID) Update product title (invalid length)
        self.assert_title('Update a Product')
        self.type('#product-name', 'This is more than 80 characters'
                  + 'asoidfjoespjfoesjopafjesopijpfes'
                  + 'ddsjsafespjesosoefjaesfp')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # (INVALID) Update product title (non-alphanumeric)
        self.assert_title('Update a Product')
        self.type('#product-name', '-_-')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # Output coverage:
        # (VALID) Title accepted
        self.assert_title('Update a Product')
        self.type('#product-name', 'Xbox One')
        self.click('input[type="submit"]')
        self.assert_title('Profile')
        self.assert_text('Welcome KWW!', '#welcome-header')

        # (INVALID) Title not accepted
        self.click('input[name="Xbox One"]')
        self.assert_title('Update a Product')
        self.type('#product-name',
                  'YABADABADOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
                  + 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO'
                  + 'OOOOOOOOOOOOOOOOOOO')
        self.click('input[type="submit"]')
        self.assert_text('Update failed.', '#message')

        # Shotgun testing
        # (VALID) Valid title
        self.assert_title('Update a Product')
        self.type('#product-name', 'NES')
        self.click('input[type="submit"]')
        self.assert_title('Profile')
        self.assert_text('Welcome KWW!', '#welcome-header')

        # (INVALID) Invalid title
        self.click('input[name="NES"]')
        self.assert_title('Update a Product')
        self.type('#product-name', '__')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

    def test_update_product_r4_3_description(self, *_):
        """
        R4-3: The description of the product can be arbitrary characters,
              with a minimum length of 20 characters and a maximum of
              2000 characters.
        """

        assert register('KWW', 'rrrr@queensu.com', 'GrEgOrY1!') is True
        assert create_product('Nintendo Switch',
                              'Play all the new Nintendo games!',
                              20000, 'rrrr@queensu.com') is True
        self.open(base_url + '/login')
        self.type('#email', 'rrrr@queensu.com')
        self.type('#password', 'GrEgOrY1!')
        self.click('input[type="submit"]')
        self.assert_title('Profile')

        # Input coverage
        # R4-3 (VALID) Update description (valid description length)
        self.click('input[name="Nintendo Switch"]')
        self.assert_title('Update a Product')
        self.type('#description', 'This console is indeed really cool.')
        self.click('input[type="submit"]')
        self.assert_title('Profile')
        self.assert_text('Welcome KWW!', '#welcome-header')

        # R4-3 (INVALID) Update descripiton (too short of a description length)
        self.click('input[name="Nintendo Switch"]')
        self.assert_title('Update a Product')
        self.type('#description', 'Not big enough')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # R4-3 (INVALID) Update descripiton (too long of a description length)
        self.assert_title('Update a Product')
        self.type('#description',
                  'Super Mario Bros. 2 is a platform video '
                  + 'game developed and published by '
                  + 'Nintendo for the Nintendo Entertainment '
                  + 'System. The game was first released in '
                  + 'North America in October 1988, and in '
                  + 'the PAL region the following year. It '
                  + 'has been remade or re-released for '
                  + 'several video game consoles. The '
                  + 'Western release of Super Mario Bros. 2 '
                  + 'was based on Yume K: Doki Doki '
                  + 'Panic, a Family Computer Disk System '
                  + 'game meant to tie-in with Fuji '
                  + "Television's media technology expo, "
                  + 'called Yume K (lit. Dream Factory). '
                  + 'The characters, enemies, and themes of '
                  + 'the game were meant to reflect the '
                  + 'mascots and theme of the festival. After'
                  + ' Nintendo of America found the Japanese '
                  + 'version of Super Mario Bros. 2 (later '
                  + 'released internationally as Super Mario '
                  + 'Bros.: The Lost Levels) to be too '
                  + 'difficult and similar to its '
                  + 'predecessor, Yume K: Doki Doki Panic '
                  + 'was modified to become Super Mario '
                  + 'Bros. 2 for release outside of Japan. A '
                  + 'commercial success, the international '
                  + 'Super Mario Bros. 2 was re-released in '
                  + 'Japan for the Famicom as Super Mario '
                  + 'USA (1992), as part of the Super Mario '
                  + 'All-Stars (1993) collection for the '
                  + 'Super NES (including the Japanese Super '
                  + 'Mario Bros. 2 as The Lost Levels), and '
                  + 'as Super Mario Advance (2001) for the '
                  + 'Game Boy Advance. Gameplay: Super Mario '
                  + 'Bros. 2 is a 2D side-scrolling platform '
                  + 'game. The objective of the game is to '
                  + "navigate the player's character through "
                  + 'the dream world Subcon and defeat the '
                  + 'main antagonist Wart. Before each '
                  + 'stage, the player chooses one of four '
                  + 'different protagonists to use: Mario, '
                  + 'Luigi, Toad, and Princess Toadstool. '
                  + 'Unlike the previous game, this game '
                  + 'does not have multiplayer functionality. '
                  + 'There is also no time limit to complete '
                  + 'any level. All four characters can run, '
                  + 'jump, and climb ladders or vines, but '
                  + 'each character possesses a unique '
                  + 'strength that causes them to be '
                  + 'controlled differently. For example, '
                  + 'Luigi can jump the highest; Princess '
                  + "Toadstool can float; Toad's strength "
                  + 'allows him to pick up items quickly; '
                  + 'and Mario represents the best balance '
                  + 'between jumping and strength. As '
                  + 'opposed to the original Super Mario '
                  + 'Bros., which only moved from left to '
                  + 'right, players can move either left or '
                  + 'right, as well as vertically in '
                  + 'waterfall, cloud and cave levels.')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # Output coverage
        # Valid description
        self.assert_title('Update a Product')
        self.type('#description', 'This is a valid description.')
        self.click('input[type="submit"]')
        self.assert_title('Profile')
        self.assert_text('Welcome KWW!', '#welcome-header')

        # Invalid description
        self.click('input[name="Nintendo Switch"]')
        self.assert_title('Update a Product')
        self.type('#description', 'Not valid.')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

    def test_update_product_r5_2_r5_5_price(self, *_):
        """
        R4-5: Price has to be of range [10, 10000].

        R5-2: Price can be only increased but cannot be decreased.
        """

        assert register('KWW', 'eeee@queensu.com', 'GrEgOrY1!') is True
        assert create_product('Baseball Bat',
                              'Play a grand ol game of ball with this bat!',
                              1000, 'eeee@queensu.com') is True
        self.open(base_url + '/login')
        self.type('#email', 'eeee@queensu.com')
        self.type('#password', 'GrEgOrY1!')
        self.click('input[type="submit"]')
        self.assert_title('Profile')

        # Input coverage:
        # R4-5 and R5-2 (VALID) Update price (valid price value)

        self.click('input[name="Baseball Bat"]')
        self.assert_title('Update a Product')
        self.type('#price', '12')
        self.click('input[type="submit"]')
        self.assert_title('Profile')
        self.assert_text('Welcome KWW!', '#welcome-header')

        # R4-5 (INVALID) Update price (invalid price value)
        self.click('input[name="Baseball Bat"]')
        self.assert_title('Update a Product')
        self.type('#price', '9')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # R4-5 (INVALID) Update price (invalid price value)
        self.assert_title('Update a Product')
        self.type('#price', '10001')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # R5-2 (INVALID) Update price (updated price value is not greater
        # than price value)
        self.assert_title('Update a Product')
        self.type('#price', '10')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')

        # Output coverage
        # Valid price
        self.assert_title('Update a Product')
        self.type('#price', '100')
        self.click('input[type="submit"]')
        self.assert_title('Profile')
        self.assert_text('Welcome KWW!', '#welcome-header')

        # Invalid price
        self.click('input[name="Baseball Bat"]')
        self.assert_title('Update a Product')
        self.type('#price', '5')
        self.click('input[type="submit"]')
        self.assert_title('Update a Product')
        self.assert_text('Update failed.', '#message')
