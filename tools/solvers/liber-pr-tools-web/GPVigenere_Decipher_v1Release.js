// Gematria Prime Vigenere Decipherer
// Version 1 Release Version March 16, 2021. 
// This program was made by Angelo Fiore. email: beautifulevilflower@gmail.com



function Rune ( input) { //the "runic" character for each value is printed in output
    switch (input) {      //to make cypher words more easy to discover
    case 0:               //by making the juxtapostion of the runes used more conveniently accessible
        return "F";
        break;
    case 1:
        return "U";
        break;
    case 2:
        return "TH";
        break;
    case 3:
        return "O";
        break;
    case 4:
        return "R";
        break;
    case 5:
        return "C/K";
        break;
    case 6:
        return "G";
        break;
    case 7:
        return "W";
        break;
    case 8:
        return "H";
        break;
    case 9:
        return "N";
        break;
    case 10:
        return "I";
        break;
    case 11:
        return "J";
        break;
    case 12:
        return "EO";
        break;
    case 13:
        return "P";
        break;
    case 14:
        return "X";
        break;
    case 15:
        return "S/Z";
        break;
    case 16:
        return "T";
        break;
    case 17:
        return "B";
        break;
    case 18:
        return "E";
        break;
    case 19:
        return "M";
        break;
    case 20:
        return "L";
        break;
    case 21:
        return "NG/ING";
        break;
    case 22:
        return "OE";
        break;
    case 23:
        return "D";
        break;
    case 24:
        return "A";
        break;
    case 25:
        return "AE";
        break;
    case 26:
        return "Y";
        break;
    case 27:
        return "IA/IO";
        break;
    case 28:
        return "EA";
        break;
    default:
        return "Error: Out of Range";
    }
}


async function main()
{
    let raw_input = ""; //the input is a string to make easier error handling for nonnumerical inputs
    let input_value = 0; //converted value of input string to an int
    let is_number = 1; //equals zero if input is not a number

    cout("Gematria Prime Vigenere Decipherer\nVersion 1 Release Version March 16, 2021.\nThis program was made by Angelo Fiore. email: beautifulevilflower@gmail.com" + endl
         + "This is a calculator for Vigenere cipher values of the Gemtria Prime\nEnter a rune\'s value from 0 to 28, then press \"enter\".\n\nYour Input:");
  
    for (;;) {
        //this loop handles the error caused by nonnumerical input
        //without this loop nonnumerical input can crash the program
        do {
            is_number = 1;
            raw_input = await cin();//cin >> raw_input;
            try { input_value = stoi(raw_input); }
            catch (ia) {
                is_number = 0;
                cout("Your entry is invalid.  Please enter a value between 0 and 28.\nYour Input:");
            }
        } while (!is_number);
        //this loop ensures that calculations are only made for a value corresponding to a "rune" in the "Gematria Prime" cipher
        //the intention is to reduce the likelihood of a miscalculation based on a typo
        while ((0 > input_value || input_value > 28)) {
            cout("Your entry is invalid.  Please enter a value between 0 and 28.\nYour Input:");
            raw_input = await cin();
            input_value = stoi(raw_input);
        }
        //calculations are made by iteration
        //for each iteration a given value between 0 and 28 is simultaneously added and subtracted from the value of the input
        //the values of each iteration's addition & subtraction are printed side by side
        //allowing one to more easily compare and navigate values
        for (let i = 0; i < 29; i++) {
            let buffer_sum = 0;
            let buffer_reduce = 0;
            buffer_sum = input_value + i;
            if (buffer_sum > 28) {
                buffer_sum -= 28;
            }
            buffer_reduce = input_value - i;
            if (buffer_reduce < 0) {
                buffer_reduce += 28;
            }
            cout(raw_input + " (is " + Rune(input_value) + ")" + " + " + i + " (is " + Rune(i) + ")" + " = " + buffer_sum + " (is " + Rune(buffer_sum) + ")" + "\t"
                 + raw_input + " (is " + Rune(input_value) + ")" + " - " + i + " (is " + Rune(i) + ")" + " = " + buffer_reduce + " (is " + Rune(buffer_reduce) + ")" + endl);
        }
        cout("Your Input:");
    }
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
