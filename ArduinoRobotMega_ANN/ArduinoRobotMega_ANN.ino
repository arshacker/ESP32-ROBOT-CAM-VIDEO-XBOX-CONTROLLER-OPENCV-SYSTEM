
// This is the sketch for the Slave Arduino using the hardware I2C.
//ANN 1
#include <Arduino.h>   //oled
#include <U8g2lib.h>   //oled

#include <Wire.h>

#include <SPI.h>   //spi oled

volatile byte buffer[40];
volatile int rxHowMany;
volatile int rxInterrupts = 0;
volatile boolean flagRequest;

signed short int bufSigned[40];
byte TXbuf[] = { 101, 20, 110, 5, 100, 105, 44, 2, 120, 72 }; //ars

int bufInt[40];
int printOnce = 0;

//char basciibuf[20];

U8G2_SH1106_128X64_NONAME_F_4W_HW_SPI u8g2(U8G2_R0, /* cs=*/ 53, /* dc=*/ 9, /* reset=*/ 8);  //clk pin 13 UNO mosi pin 11 UNO 

//ANN OLED
void ipPrint(void){
  int a = bufSigned[0];
  char asciibuf[20]={0,};
  int b = bufSigned[1];
  int c = bufSigned[2];
  int d = bufSigned[3];
  
  //char bsciibuf[3];
  itoa(a,asciibuf,10); //10 is decimal
  itoa(b,asciibuf+4,10);
  itoa(c,asciibuf+8,10);
  itoa(d,asciibuf+12,10);

//  itoa(c,basciibuf,10);

  //asciibuf[4]=" ";
  

  char totalbuf[20];
  totalbuf[0]=asciibuf[0];
  totalbuf[1]=asciibuf[1];
  totalbuf[2]=asciibuf[2];
  totalbuf[3]=asciibuf[4];
  totalbuf[4]=asciibuf[5];
  totalbuf[5]=asciibuf[6];
  totalbuf[6]=asciibuf[7];

  //String myStr1 = String(bufSigned[0]);

  //ug82.drawStr(xcoord=5 x nbr spaces,ycoord=10 x nbr lines,"STRING")
  
  u8g2.clearBuffer();          // clear the internal memory
  u8g2.setFont(u8g2_font_ncenB08_tr); // choose a suitable font
  u8g2.drawStr(0,10,"IP ADDRESS");  // write 1ST LINE to the internal memory
  u8g2.drawStr(0,20,asciibuf);  // write 2ND LINE to the internal memory
  //u8g2.drawStr(0,20,myStr1);  // write 2ND LINE to the internal memory
  u8g2.drawStr(25,20,asciibuf+4);  // write 2ND LINE to the internal memory
  u8g2.drawStr(50,20,asciibuf+8);  // write 2ND LINE to the internal memory//NEW
  u8g2.drawStr(75,20,asciibuf+12);  // write 2ND LINE to the internal memory//NEW    
  //u8g2.drawStr(50,20,asciibuf+4);  // EVEN THIS DOESNT WORK???
  //u8g2.drawStr(50,20,asciibuf+8);  // write 2ND LINE to the internal memory
  //u8g2.drawStr(50,20,"K");
  //u8g2.drawStr(45,20,basciibuf);  // write 2ND LINE to the internal memory
  //u8g2.drawStr(0,30,asciibuf+4);  // write 2ND LINE to the internal memory
  //u8g2.drawStr(0,40,asciibuf+8);  // write 2ND LINE to the internal memory
  //u8g2.drawStr(25,40,asciibuf+12);  // write 2ND LINE to the internal memory
  //u8g2.drawStr(0,50,asciibuf+12);  // write 2ND LINE to the internal memory
  u8g2.drawStr(0,30,"SIGN IN NOW!");  // write LAST LINE to the internal memory
  u8g2.sendBuffer();          // transfer internal memory to the display
  delay(1000);   
}

void testPrint(void){
  u8g2.clearBuffer();          // clear the internal memory
  u8g2.setFont(u8g2_font_ncenB08_tr); // choose a suitable font
  u8g2.drawStr(0,10,"Hello World!");  // write 1ST LINE to the internal memory
  u8g2.drawStr(0,20,"Hello Again World!");  // write 2ND LINE to the internal memory
  u8g2.drawStr(0,60,"Bye For Now World!");  // write LAST LINE to the internal memory
  u8g2.sendBuffer();          // transfer internal memory to the display
  delay(1000);   
}

//ANN 2
void requestEvent()
{
  static byte x = 0;
  
  // Fill array with numbers.

  TXbuf[2] = buffer[23];
   
  //TXbuf[0] = x++;         // overwrite the first with a counter.
  Wire.write(TXbuf, sizeof(TXbuf));
  
  flagRequest = true;
}


//ANN 3
void receiveEvent(int howMany)   //HOWMANY BYTES SENT BY MASTER--5 BYTES //ars
{
  for( int i=0; i<howMany; i++)
    buffer[i] = Wire.read();
  
  rxHowMany = howMany;
  rxInterrupts++;
}

void setup()
{
  Serial.begin(115200);           // start serial for output
  Serial.println("\nSlave");

  Wire.begin(4);                // join i2c bus as slave with address #4
  Wire.onReceive(receiveEvent); // interrupt handler for receiving i2c data
  Wire.onRequest(requestEvent); // interrupt handler for when data is requested by i2c
  for(int y=0; y<40; y++){
    bufSigned[y] = 0;
  }
  u8g2.begin();   //oled
  delay(10);
  //testPrint();
}

//ANN 4
void loop()
{
  delay(2000);
  noInterrupts();
  int rxInterruptsCopy = rxInterrupts;
  rxInterrupts = 0;
  interrupts();

  if(printOnce==0 && bufSigned[0]!=0){
    ipPrint();
    printOnce=0;
  }
  

  //TXbuf[0]++;
  //if(TXbuf[0]==128)
  //  {TXbuf[0] = 0;}
  
  // Using all the text output to the Serial port is part of the stress test.
  // That causes delays and interrupts.
  if( rxInterruptsCopy > 0)
  {
    Serial.print("Receive: ");
    /*
    if( rxInterruptsCopy > 1) //BY TIME LOOP CAME AROUND,MORE THAN 1 RCV IRPT-MISSED THOSE
    {
      // Printing to the serial port at 9600 is slow.
      // Therefor it is normal that this sketch misses received data,
      // if too much data was received.
      // As long as the i2c data is correct, everything is okay. It is a stress test.
      Serial.print("Missed:");
      Serial.print( rxInterruptsCopy);
      Serial.print(" ");
    }
    */
    Serial.print("howMany:");
    Serial.print( rxHowMany);
    
    Serial.print(", data:");
    for(int i=0; i<rxHowMany; i++)
    {
      if( i == 0)
        Serial.print(F("*"));      // indicate the first number (sometimes used for a counter value).

      Serial.print((unsigned int) buffer[i], DEC);
      Serial.print(" ");
    }
    Serial.println();
  }


    convertToSigned();  

    Serial.print("BUFSIGNED = ");
    for(int i=0; i<rxHowMany; i++)
    {
      //if( i == 0)
      //  Serial.print(F("*"));      // indicate the first number (sometimes used for a counter value).

      Serial.print(bufSigned[i], DEC);
      Serial.print(" ");
    }
    Serial.println();

    Serial.print("TXBUF = ");
    for( int m=0; m<10; m++)
    {  
      if( m == 0)
        Serial.print(F("*"));      // indicate the number of the counter
      Serial.print( (int) TXbuf[m]);
      Serial.print(F(", "));
    }
    Serial.println();
    

  //bufInt[0] = (char)buffer[0].toInt();
  Serial.print("BUFFER = ");
  Serial.println(buffer[0]+1);
  
  noInterrupts();
  boolean flagRequestCopy = flagRequest;
  flagRequest = false;
  interrupts();
  
  if( flagRequestCopy)
  {
    Serial.println("Request: Data was requested and send");
  }
  
  // Stress the master by disabling interrupts.
  // A value of 500 microseconds will even corrupt the transmission with the normal Arduino Wire library.
  //noInterrupts();            //ARS 3 LINES DONT STRESS
  //delayMicroseconds(50);     //ARS DONT STRESS
  //interrupts();              //ARS DONT STRESS
}




void convertToSigned(void){
  for(int t=0; t<4; t++){      //first 4 elem of buffer are pos ip nbrs
     bufSigned[t] = buffer[t];
    }
  
  for(int t=4; t<39; t++){   //first 4 elem of buffer are pos ip nbrs
     if(buffer[t]>128){
         bufSigned[t] = -256 + buffer[t];
      }
      else
         bufSigned[t] = buffer[t];
    
    }
} 



