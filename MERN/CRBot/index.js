const { Configuration, OpenAIApi } = require('openai');

const config = new Configuration({
	apiKey: 'SECRETKEY',
});

const openai = new OpenAIApi(config);

const getCodeReview = async (strPromptText) => {
	try {
		const response = await openai.createCompletion({
			model: 'text-davinci-003',
			prompt: strPromptText,
			max_tokens: 2048,
			temperature: 1,
		});
		console.log(response.data.choices[0].text);
	} catch (error) {
		console.log('Error:', error.message);
	}
};

const strPromptText = `

Here are some points you need to keep in mind while reviewing the code:
1. Remember to include white space after opening and before closing brackets either its (), {}, or [] if there is something written between them.
2. Remember to include white space after and before any operators like +, -, *, /, %, ^, =, +=, -=, *=, /=, .=, etc if there is something written before or after it.
3. Variables name must have prefixes based on their data type. For instance, you can use $int for variables that store integers, $str for variables that store strings, $arr for variables that store arrays, $arrint for variables that store arrays of integers, $arrstr for variables that store arrays of strings, $arrbj for variables that store arrays of objects, $obj for variables that store objects, etc. By following this naming convention, it'll be easier to read and understand the code.
4. When writing conditions, if there is any value that is being compared with a constant, the constant should be placed before the variable that is being compared.
5. Apart from the above four points, feel free to suggest any additional logical code changes or optimizations that may improve the code's efficiency or readability.

Example 1:
    Input:    
    function getSum($intFirstNumber, $intSecondNumber){
        return $intFirstNumber+$intSecondNumber;
    }

    Output:
    Feedback:
    1. You have missed white spaces before and after different brackets.
    2. You have missed white spaces before and after operator.
    3. Use meaningful function name that describe their purpose in the code. This makes it easier for others to understand the code without having to read through comments or documentation.

    Updated code can be written like this:
    function getSumOfTwoNumbers( $intFirstNumber, $intSecondNumber ) {
        return $intFirstNumber + $intSecondNumber;
    }

Example 2:
    Input:
    function getFullName( $firstName, $secondName ){
        return ( $firstName+$secondName );
    }
    
    $firstName = 'Sachin';
    $secondName = 'Saurav';
    echo getFullName($firstName, $secondName);

    Output:
    Feedback:
    1. You have missed white spaces between two different brackets.
    2. You have missed white spaces before and after operator.
    3. You haven't added a prefixes to variable names based on their data type. This makes it easier for others to understand the code. As $firstName and $secondName is of string data type, they can be renamed to $strFirstName and $strSecondName.
    4. Consider using comments to explain the purpose of your code or certain functions to make it easier for others to follow code flow.

    Updated code can be written like this:
    // This function will return full name by concatenating give first and last name 
    function getFullName( $strFirstName, $strFirstName){
        return ( $strFirstName + $strSecondName );
    }

    // working example
    $strFirstName = 'Sachin';
    $strSecondName = 'Saurav';
  
    $echo getFullName($strFirstName, $strSecondName);

Example 3:
    Input:
    function addMonthsToDate( $date, $months ) {
        return date( 'm/d/Y", strtotime( '+' . $months . 'months', $date ) );
    }

    // demo
    $date = '02/13/2023';
    $months = 1;
    echo addMonthsToDate( $date, $months );

Output:
Feedback:
1. You haven't added prefixes to variable names based on their data type. This makes it easier for others to understand the code. As $date is of string data type and $months is of integer type, they can be renamed to $strDate and $intMonths.
2. It's a good practice to check the validity of the input date before using it in any function.
3. As the DateTime class is more powerful and flexible, and can be a better choice for more complex date calculations or when you need to work with time zones. You can use DateTime::createFromFormat instead of strtotime.

    Updated code can be written like this:
    function addMonthsToDate( $strDate, $intMonths ) {
        $strDate = DateTime::createFromFormat( 'm/d/Y', $strDate );
        if ( !$strDate ) {
            return false;
        }
        $strDate->modify( " + $intMonths months" );

        return $date->format( 'm/d/Y' );
    }

    // demo
    $strDate = '02/13/2023';
    $intMonths = 1;
    echo addMonthsToDate( $strDate, $intMonths );

?>

Example 4:
    Input:
    function getUserType( $strName ) {
        if ( $strName == 'Sachin' ) {
            return 'Super Admin';
        } else if ( $strName == 'Saurav' ) {
            return 'Admin';
        } else {
            return 'General User';
        }
    }

    Output:
    Feedback:
    1. When writing conditions, if there is any value that is being compared with a constant, the constant should be placed before the variable that is being compared.

    Updated code can be written like this:
    function getUserType( $strName ) {
        if ( 'Sachin' == $strName ) {
            return 'Super Admin';
        } else if ( 'Saurav' == $strName ) {
            return 'Admin';
        } else {
            return 'General User';
        }
    }

Example 5:
    Input: 
    function getReverseString($text){
        for($i=strlen($text)-1, $j=0; $j<$i; $i--, $j++){
            $temp = $text[$i];
            $text[$i] = $text[$j];
            $text[$j] = $temp;
        }
        return $text;
    }

    // Driver code
    $text = "entrata";
    print_r( getReverseString( $text ) );

    Output:
    The code looks fine and optimized. But to make it more readable, we can make few improvements:

    Feedback:
    1. You have missed white spaces before and after different brackets.
    2. You have missed white spaces before and after operator.
    3. Use meaningful variable name that describe their purpose in the code. This makes it easier for others to understand the code without having to read through comments or documentation.
    4. Consider using comments to explain the purpose of your code or certain functions to make it easier for others to follow code flow.
    
    So, the final optimized code could look like this:

    // This function will return a given string in reverse order
    function getReverseString( $strText ) {

        //this loop will reverse the provided string
        for( $intIndexFirst = strlen( $strText ) - 1, $intIndexSecond = 0; $intIndexSecond < $intIndexFirst; $intIndexFirst--, $intIndexSecond++ ) {
            $strTemp = $strText[$intIndexFirst];
            $strText[$intIndexFirst] = $strText[$intIndexSecond];
            $strText[$intIndexSecond] = $strTemp;
        }

        return $strText;
    }
    
    // example to show reverse of a string
    $strText = "entrata";
    print_r( getReverseString( $strText ) );

    Can you review the below code snippet?
    <?php
        // Function to check for Palindrome number
        function Palindrome($number){
            $temp = $number;
            $new = 0;
            while (floor($temp)) {
                $d = $temp % 10;
                $new = $new * 10 + $d;
                $temp = $temp/10;
            }
            if ($new == $number){
                return 1;
            }
            else{
                return 0;
            }
        }

        // Driver Code
        $original = 1441;
        if (Palindrome($original)){
            echo "Palindrome";
        }
        else {
        echo "Not a Palindrome";
        }

    ?>

`;

console.clear();
getCodeReview(strPromptText);
