int SER_Pin = 8; //pin 14 on the 75HC595
int RCLK_Pin = 9; //pin 12 on the 75HC595
int SRCLK_Pin = 10; //pin 11 on the 75HC595

char incomingByte;

//Number of shift registers
#define number_of_74hc595s 12

//do not touch
#define numOfRegisterPins number_of_74hc595s * 8

boolean registers[numOfRegisterPins];

void setup(){
  Serial.begin(9600);
  
  pinMode(SER_Pin, OUTPUT);
  pinMode(RCLK_Pin, OUTPUT);
  pinMode(SRCLK_Pin, OUTPUT);

  //reset all register pins
  clearRegisters();
  writeRegisters();
}

//set all register pins to LOW
void clearRegisters(){
  for(int i = numOfRegisterPins - 1; i >= 0; i--){
    registers[i] = LOW;
  }
}

//Set and display registers
//Only call AFTER all values are set how you would like (slow otherwise)
void writeRegisters(){

  digitalWrite(RCLK_Pin, LOW);

  for(int i = numOfRegisterPins - 1; i >= 0; i--){
    digitalWrite(SRCLK_Pin, LOW);

    int val = registers[i];

    digitalWrite(SER_Pin, val);
    digitalWrite(SRCLK_Pin, HIGH);

  }
  digitalWrite(RCLK_Pin, HIGH);

}

//set an individual pin HIGH or LOW
void setRegisterPin(int index, int value){
  registers[index] = value;
}


void loop(){

  //send message back to confirm message
  if(Serial.available() > 0) {
    incomingByte = Serial.read();

    Serial.print("I received: ");
    Serial.println(incomingByte);
  }

  //first five bits represent fret (1-15))
  //remaining bits represent string (1-6)
  switch(incomingByte) {
    case 0b00000001: {  //Fret 0, String 1 (open string)
      setRegisterPin(0, HIGH);
      break;
    }
    case 0b00000010: {  //Fret 0, String 2 (open string)
      setRegisterPin(1, HIGH);
      break;
    }
    case 0b00000011: {  //Fret 0, String 3 (open string)
      setRegisterPin(2, HIGH);
      break;
    }
    case 0b00000100:  { //Fret 0, String 4 (open string)
      setRegisterPin(3, HIGH);
      break;
    }
    case 0b00000101:  { //Fret 0, String 5 (open string)
      setRegisterPin(4, HIGH);
      break;
    }
    case 0b00000110: {  //Fret 0, String 6 (open string)
      setRegisterPin(5, HIGH);
      break;
    }
    case 0b00001001: {  //Fret 1, String 1
      setRegisterPin(6, HIGH);
      break;
    }
    case 0b00001010: {  //Fret 1, String 2
      setRegisterPin(7, HIGH);
      break;
    }
    case 0b00001011: {  //Fret 1, String 3
      setRegisterPin(8, HIGH);
      break;
    }
    case 0b00001100: {  //Fret 1, String 4
      setRegisterPin(9, HIGH);
      break;
    }
    case 0b00001101: { //Fret 1, String 5
      setRegisterPin(10, HIGH);
      break;
    }
    case 0b00001110: {  //Fret 1, String 6
      setRegisterPin(11, HIGH);
      break;
    }
    case 0b00010001: {  //Fret 2, String 1
      setRegisterPin(12, HIGH);
      break;
    }
    case 0b00010010: {  //Fret 2, String 2
      setRegisterPin(13, HIGH);
      break;
    }
    case 0b00010011: {  //Fret 2, String 3
      setRegisterPin(14, HIGH);
      break;
    }
    case 0b00010100: {  //Fret 2, String 4
      setRegisterPin(15, HIGH);
      break;
    }
    case 0b00010101: {  //Fret 2, String 5
      setRegisterPin(16, HIGH);
      break;
    }
    case 0b00010110: {  //Fret 2, String 6
      setRegisterPin(17, HIGH);
      break;
    }
    case 0b00011001: {  //Fret 3, String 1
      setRegisterPin(18, HIGH);
      break;
    }
    case 0b00011010:  { //Fret 3, String 2
      setRegisterPin(19, HIGH);
      break;
    }
    case 0b00011011:  { //Fret 3, String 3
      setRegisterPin(20, HIGH);
      break;
    }
    case 0b00011100: {  //Fret 3, String 4
      setRegisterPin(21, HIGH);
      break;
    }
    case 0b00011101: {  //Fret 3, String 5
      setRegisterPin(22, HIGH);
      break;
    }
    case 0b00011110: {  //Fret 3, String 6
      setRegisterPin(23, HIGH);
      break;
    }
    case 0b00100001: {  //Fret 4, String 1
      setRegisterPin(24, HIGH);
      break;
    }
    case 0b00100010: {  //Fret 4, String 2
      setRegisterPin(25, HIGH);
      break;
    }
    case 0b00100011: { //Fret 4, String 3
      setRegisterPin(26, HIGH);
      break;
    }
    case 0b00100100: {  //Fret 4, String 4
      setRegisterPin(27, HIGH);
      break;
    }
    case 0b00100101: {  //Fret 4, String 5
      setRegisterPin(28, HIGH);
      break;
    }
    case 0b00100110: {  //Fret 4, String 6
      setRegisterPin(29, HIGH);
      break;
    }
    case 0b00101001: {  //Fret 5, String 1
      setRegisterPin(30, HIGH);
      break;
    }
    case 0b00101010: {  //Fret 5, String 2
      setRegisterPin(31, HIGH);
      break;
    }
    case 0b00101011: {  //Fret 5, String 3
      setRegisterPin(32, HIGH);
      break;
    }
    case 0b00101100: {  //Fret 5, String 4
      setRegisterPin(33, HIGH);
      break;
    }
    case 0b00101101: {  //Fret 5, String 5
      setRegisterPin(34, HIGH);
      break;
    }
    case 0b00101110:  { //Fret 5, String 6
      setRegisterPin(35, HIGH);
      break;
    }
    case 0b00110001:  { //Fret 6, String 1
      setRegisterPin(36, HIGH);
      break;
    }
    case 0b00110010: {  //Fret 6, String 2
      setRegisterPin(37, HIGH);
      break;
    }
    case 0b00110011: {  //Fret 6, String 3
      setRegisterPin(38, HIGH);
      break;
    }
    case 0b00110100: {  //Fret 6, String 4
      setRegisterPin(39, HIGH);
      break;
    }
    case 0b00110101: {  //Fret 6, String 5
      setRegisterPin(40, HIGH);
      break;
    }
    case 0b00110110: {  //Fret 6, String 6
      setRegisterPin(41, HIGH);
      break;
    }
    case 0b00111001: { //Fret 7, String 1
      setRegisterPin(42, HIGH);
      break;
    }
    case 0b00111010: {  //Fret 7, String 2
      setRegisterPin(43, HIGH);
      break;
    }
    case 0b00111011: {  //Fret 7, String 3
      setRegisterPin(44, HIGH);
      break;
    }
    case 0b00111100: {  //Fret 7, String 4
      setRegisterPin(45, HIGH);
      break;
    }
    case 0b00111101: {  //Fret 7, String 5
      setRegisterPin(46, HIGH);
      break;
    }
    case 0b00111110: {  //Fret 7, String 6
      setRegisterPin(47, HIGH);
      break;
    }
    case 0b01000001: {  //Fret 8, String 1
      setRegisterPin(48, HIGH);
      break;
    }
    case 0b01000010: {  //Fret 8, String 2
      setRegisterPin(49, HIGH);
      break;
    }
    case 0b01000011: {  //Fret 8, String 3
      setRegisterPin(50, HIGH);
      break;
    }
    case 0b01000100:  { //Fret 8, String 4
      setRegisterPin(51, HIGH);
      break;
    }
    case 0b01000101:  { //Fret 8, String 5
      setRegisterPin(52, HIGH);
      break;
    }
    case 0b01000110: {  //Fret 8, String 6
      setRegisterPin(53, HIGH);
      break;
    }
    case 0b01001001: {  //Fret 9, String 1
      setRegisterPin(54, HIGH);
      break;
    }
    case 0b01001010: {  //Fret 9, String 2
      setRegisterPin(55, HIGH);
      break;
    }
    case 0b01001011: {  //Fret 9, String 3
      setRegisterPin(56, HIGH);
      break;
    }
    case 0b01001100: {  //Fret 9, String 4
      setRegisterPin(57, HIGH);
      break;
    }
    case 0b01001101: { //Fret 9, String 5
      setRegisterPin(58, HIGH);
      break;
    }
    case 0b01001110: {  //Fret 9, String 6
      setRegisterPin(59, HIGH);
      break;
    }
    case 0b01010001: {  //Fret 10, String 1
      setRegisterPin(60, HIGH);
      break;
    }
    case 0b01010010: {  //Fret 10, String 2
      setRegisterPin(61, HIGH);
      break;
    }
    case 0b01010011: {  //Fret 10, String 3
      setRegisterPin(62, HIGH);
      break;
    }
    case 0b01010100: {  //Fret 10, String 4
      setRegisterPin(63, HIGH);
      break;
    }
    case 0b01010101: {  //Fret 10, String 5
      setRegisterPin(64, HIGH);
      break;
    }
    case 0b01010110: {  //Fret 10, String 6
      setRegisterPin(65, HIGH);
      break;
    }
    case 0b01011001: {  //Fret 11, String 1
      setRegisterPin(66, HIGH);
      break;
    }
    case 0b01011010:  { //Fret 11, String 2
      setRegisterPin(67, HIGH);
      break;
    }
    case 0b01011011:  { //Fret 11, String 3
      setRegisterPin(68, HIGH);
      break;
    }
    case 0b01011100: {  //Fret 11, String 4
      setRegisterPin(69, HIGH);
      break;
    }
    case 0b01011101: {  //Fret 11, String 5
      setRegisterPin(70, HIGH);
      break;
    }
    case 0b01011110: {  //Fret 11, String 6
      setRegisterPin(71, HIGH);
      break;
    }
    case 0b01100001: {  //Fret 12, String 1
      setRegisterPin(72, HIGH);
      break;
    }
    case 0b01100010: {  //Fret 12, String 2
      setRegisterPin(73, HIGH);
      break;
    }
    case 0b01100011: { //Fret 12, String 3
      setRegisterPin(74, HIGH);
      break;
    }
    case 0b01100100: {  //Fret 12, String 4
      setRegisterPin(75, HIGH);
      break;
    }
    case 0b01100101: {  //Fret 12, String 5
      setRegisterPin(76, HIGH);
      break;
    }
    case 0b01100110: {  //Fret 12, String 6
      setRegisterPin(77, HIGH);
      break;
    }
    case 0b01101001: {  //Fret 13, String 1
      setRegisterPin(78, HIGH);
      break;
    }
    case 0b01101010: {  //Fret 13, String 2
      setRegisterPin(79, HIGH);
      break;
    }
    case 0b01101011: {  //Fret 13, String 3
      setRegisterPin(80, HIGH);
      break;
    }
    case 0b01101100: {  //Fret 13, String 4
      setRegisterPin(81, HIGH);
      break;
    }
    case 0b01101101: {  //Fret 13, String 5
      setRegisterPin(82, HIGH);
      break;
    }
    case 0b01101110:  { //Fret 13, String 6
      setRegisterPin(83, HIGH);
      break;
    }
    case 0b01110001:  { //Fret 14, String 1
      setRegisterPin(84, HIGH);
      break;
    }
    case 0b01110010: {  //Fret 14, String 2
      setRegisterPin(85, HIGH);
      break;
    }
    case 0b01110011: {  //Fret 14, String 3
      setRegisterPin(86, HIGH);
      break;
    }
    case 0b01110100: {  //Fret 14, String 4
      setRegisterPin(87, HIGH);
      break;
    }
    case 0b01110101: {  //Fret 14, String 5
      setRegisterPin(88, HIGH);
      break;
    }
    case 0b01110110: {  //Fret 14, String 6
      setRegisterPin(89, HIGH);
      break;
    }
    default: clearRegisters();
  }

  writeRegisters(); //MUST BE CALLED TO DISPLAY CHANGES
}
