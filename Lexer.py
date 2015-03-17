from pygments.lexers.css import ScssLexer
from TokenGroup import TokenGroup

scssLexer = ScssLexer()
scss = '''
@import 'base';
@import 'this should not be on the bottom';

button, select, input[type="submit"] {
    /* test */
    $blue_dark: #369;
    // Important container
    $container_width: 50px;
    $blue_light: rgba(196, 219, 241, 1);
    @extend 'poop';
    @extend 'something else too';
    @include mq($from:small) {
        color: red;
    }
    @extend 'something else';

    border: 1px solid $blue_light;
    /* test2 */
    border-radius: 1px;

    // We cannot forget background colors!
    background-color: white;

    color: $blue_dark;

    // Activations
    &:hover, &:active, &:focus {
        @extend 'morepoop';

        border-color: $blue_dark;
        outline: none;

        background-color: $blue_white;

        #c {
            height: 9001px;
            width: 56px;
        }
    }

    &::-webkit-input-placeholder:first-letter {
        color: red;
    }
}
'''

tokens = scssLexer.get_tokens(scss)

tokenGroup = TokenGroup()

for token in tokens:
    tokenGroup += token

print tokenGroup
