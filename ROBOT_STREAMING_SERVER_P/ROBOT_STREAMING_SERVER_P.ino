
/*********
  Parts of this code are based on the following reference.
  Rui Santos
  https://RandomNerdTutorials.com
  
  IMPORTANT!!! 
   - Select Board "ESP32 Wrover Module"
   - Select the Partion Scheme "Huge APP (3MB No OTA)
   
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  Some of the code, particularly ANN:12 below, in this program is from
  https://github.com/Dallyla/delorean-express 

*********/
//ANN 1
#include "esp_camera.h"
#include <WiFi.h>
#include "esp_timer.h"
#include "img_converters.h"
#include "Arduino.h"
#include "fb_gfx.h"
#include "soc/soc.h" //disable brownout problems
#include "soc/rtc_cntl_reg.h"  //disable brownout problems
#include "dl_lib.h"
#include "esp_http_server.h"

#include <AsyncTCP.h>
#include <ESPAsyncWebServer_ARS.h> //TOOK OUT REDEFS OF GET POST ETC IN ORIGINAL

//#define SOFTAP

/********************FROM OCV_COLORTRACK11_MS_34_3************/
//ANN 2
#include <Wire.h>    //comm to arduino
#define myWire Wire
#define SDA 14
#define SCL 13

#define SCREENCOLS 400
#define SCREENROWS 300

#define CODE_LEN 7
int code_array[CODE_LEN] = {0,0,0,0,0,0,1};
int code_nbr = 1;

//#define MSG_LEN 7  //
#define MSG_INT_LEN 5
#define MSG_LEN  2*MSG_INT_LEN-1

//char msg[MSG_LEN] = {0,};
//int msg_int[4] = {97,98,127,1}; // {97,98,127};

//char msg[MSG_LEN] = {0,};
char msg[MSG_INT_LEN] = {0,};
int msg_int[MSG_INT_LEN] = {97,98,127,1}; // {97,98,127};
                    //ALLOW POS INTEGERS 0-127

int One_Time_Transmit = 1;

int lock = 0;
char cTT[256] = {0,}; 
//char c[] = {0,};
byte d[256] = {0,};
char e;

int lenGlobal=0;

byte bufIP[4] = {0,0,0,0};  //i2c xmit
byte bufToBot[20] = {0,};  //bufToBot[19] = {0,};
byte buffer[40];             //i2c rcv(prev said transmit?
byte buffer_temp[40];    //check contents before xfr to buffer
int n = 0;                   //i2c rcv
 
int finalIndex = 0;
int initialIndex = 0;
int kIndex = 0;

long timeStart;
long timeFinish;
long timeStart1;
long timeFinish1;

int DELTA_XCM = 0;
int DELTA_YCM = 0;
byte b_Tracker = 0;
byte b_DELTA_XCM = 0;
byte b_DELTA_YCM = 0;

//ANN 3
AsyncWebServer server3(82);

AsyncWebSocket ws("/ws");

/************************start i2c transmit*************************************/
//ANN 4
  void i2cTransmit(void){
                /************SEND I2C DATA**********************/
    //Serial.println(F("Test with 1 transmissions of writing 10 bytes each"));
  //byte buf[20] = { 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, };
  byte buf[27] = { 100, 101, 102, 103, 104, 105, 106, 107, 108, 109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126};
  int err = 0;
  unsigned long millis1 = millis();
  boolean firsterr = false;
  //for( int i=0; i<1; i++)
  //{
    Serial.println(F("Sending data"));
    timeStart1 = millis();
    myWire.beginTransmission(4);

    for(int z=0; z<=3;z++){
      buf[z]=bufIP[z];
    }
    for(int v=0; v<=19; v++){
      buf[v+4]=bufToBot[v];  
    }
    buf[24] = b_DELTA_XCM;
    buf[25] = b_DELTA_YCM;
    buf[26] = b_Tracker;
    
    Serial.print("BUF = "); 
    for( int k=0; k<27; k++)
    {
    Serial.print( (int) buf[k]);
    Serial.print(F(", "));
    }
    Serial.println();
        
    myWire.write( buf, 27);       //replace with bufToBot from client
    //myWire.write(bufToBot,5);
    if( myWire.endTransmission() != 0)
    {
      err++;
    }
    delayMicroseconds(100);  // Even the normal Arduino Wire library needs some delay when the Slave disables interrupts.
 // }
    
     myWire.beginTransmission(6);
     myWire.write( buf, 27);
    if( myWire.endTransmission() != 0)
    {
      err++;
    }
    delayMicroseconds(100);  // Even the normal Arduino Wire library needs some delay when the Slave disables interrupts.
     
     
  unsigned long millis2 = millis();
  Serial.print(F("total time: "));
  Serial.print(millis2 - millis1);
  Serial.print(F(" ms, total errors: "));
  Serial.println(err);

  delay(2);
  
  timeFinish1 = millis();
  Serial.print("INNER TIME  = ");
  Serial.println(timeFinish1-timeStart1);

                             /**END SEND I2C DATA*****/

                             /**REQUEST I2C DATA******/
  
  Serial.println(F("Requesting data"));
  n = myWire.requestFrom(4, 10);    // request bytes from Slave //make n a global
  Serial.print(F("n="));
  Serial.print(n);
  Serial.print(F(", available="));
  Serial.println(myWire.available());
  
//  myWire.printStatus(Serial);      // This shows information about the SoftwareWire object.

//  byte buffer[40];         //make this a global for access by cmd func
//  for( int j=0; j<n; j++)
//    buffer[j] = myWire.read();
  myWire.readBytes( buffer_temp, n);

  Serial.print("RCV_BUFFER_TEMP = ");
  for( int k=0; k<n; k++)
  {
    if( k == 0)
      Serial.print(F("*"));      // indicate the number of the counter
    Serial.print( (int) buffer_temp[k]);
    Serial.print(F(", "));
  }
  Serial.println();

  if(buffer_temp[0]<128){                //NO ERROR
    for( int k=0; k<n; k++){
      buffer[k] = buffer_temp[k];
    }
  }

  Serial.print("RCV_BUFFER = ");
  for( int k=0; k<n; k++)
  {
    if( k == 0)
      Serial.print(F("*"));      // indicate the number of the counter
    Serial.print( (int) buffer[k]);
    Serial.print(F(", "));
  }
  Serial.println();
  
                                /***END REQUEST I2C DATA*********/                
  delay(2);
    
  }
 
 /***********************end i2c transmit**********************************/
//ANN 5
void codePrep(void){
  code_nbr = 2*2*2*2*2*2*code_array[0] + 2*2*2*2*2*code_array[1] +
             2*2*2*2*code_array[2] + 2*2*2*code_array[3]+
             2*2*code_array[4] + 2*code_array[5] + code_array[6];
  Serial.print("CODE NBR = ");
  Serial.println(code_nbr);                        
}

//ANN 6
void msgPrep(void){
  //takes msg_int[3]={X,Y,Z] and creates msg[X,',',Y,',',Z} WHERE MSG_LEN = 5
/*  
  for(int i = 1; i < MSG_LEN-2; i = i + 1){
    msg[(2*i)-1] = ',';  //comma separators for python
                         //msg[1],msg[3]...
  }  
  for(int j = 1; j < MSG_LEN-1; j = j + 1){
    if(buffer[(j-1)]!=0){
        msg[(2*j)-2] = buffer[(j-1)];
    }
    else{
        msg[(2*j)-2] = 1;     //cant transmit 0 to python?????
    }
    //msg[(2*j)-2] = msg_int[(j-1)]; //prepared message
      //msg[0]=msg_int[0],msg[2]=msg_int[1],msg[4]=msg_int[2]...
  }
 */
 //below is most recent before new strategy
 /*
  for(int i = 1; i<MSG_INT_LEN+1; i = i + 1){
    msg[(2*i)-1] = 2;  //MARKER 2 SAYS IT IS NOT ZERO
  }

  for(int i = 0; i<MSG_INT_LEN; i = i + 1){
    if (buffer[i]!=0){
      msg[2*i]=buffer[i];
    }
    else{
      msg[2*i]=1;  //cant transmit 0 (null) to python
      msg[(2*i)+1]=3;  //MARKER 3 SAYS IT SHOULD BE ZERO
    }
  }
  */

  for(int j=0; j<CODE_LEN-1; j=j+1){   //leave last location as 1
    code_array[j] = 0;                 //code_array(CODE_LEN-1)==1
  }

  for(int i = 0; i<MSG_INT_LEN; i = i + 1){
    if (buffer[i]!=0){        
      msg[i]= buffer[i];
      code_array[i] = 0;
    }
    else{
      msg[i] = 1;  //cant transmit 0 (null) to python
      code_array[i] = 1;     
    }
  }

  codePrep();
  msg[MSG_INT_LEN-1] = (char)code_nbr; //put code into MSG_INT_LEN location
  
  //Serial.print("BUFFER BUFFERR BUFFER ===");
  //Serial.println(buffer[1]); //prints a
  //msg[2] = '\x01';
  //msg[1] = 5;
  //msg[0] = buffer[0];
  //msg[2] = buffer[1];
  //msg[4] = buffer[2];
  //msg[6] = buffer[3];
}

//ANN 7
void onWsEvent(AsyncWebSocket * server3, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len){

  //msgPrep(); //comma separators  //put in ws_evt_data

  //int msg_int[] = {97,',',98,',',127}; //commas separators useful in python
  //char msg[5] = {0,}; 
  //char msg[] = {'a','b','c'};
  //char msg[] = {97,98,99};
  //char msg[] = {97,',',98,',',99};
  //char msg[] = {97,',',98,',',31};

  //msg[0] = msg_int[0]; //int to char for transmission
  //msg[1] = msg_int[1];
  //msg[2] = msg_int[2];
  //msg[3] = msg_int[3];
  //msg[4] = msg_int[4];
 
  lenGlobal = len;
  
  if(type == WS_EVT_CONNECT){
 
    Serial.println("Websocket client connection received");
    client->text("Hello from ESP32 Server3");
    //client->binary(msg); //move to ws_evt_data
 
  } else if(type == WS_EVT_DISCONNECT){
    Serial.println("Client disconnected");
 
  }else if(type==WS_EVT_DATA){
    Serial.println("Data received: ");

    for(int j=0; j < len; j++){
      d[j] = data[j];          //data read out only once allowed
      cTT[j] = d[j];  //ascii to char

            
      Serial.print(cTT[j]);   //TIMING
    }//end for j loop
    Serial.println();
    Serial.println(len);
    
    
    
    for(int i=0; i < len; i++){
      Serial.print(d[i]);     //TIMING
      Serial.print("|");
    }
    Serial.println();

    parse_msg();           //convert msg from python to array format
    initializeTT();


    msgPrep(); //comma separators
    client->binary(msg);  //return msg to python

    Serial.println("I2C Transmit");
    i2cTransmit();
    initializeTT();    

   }//end else if ws evt data
}//end onwsevent


void initializeTT(void)
{
  for(int n=0;n<256;n++){
    cTT[n] = 0;
    d[n] = 0;
   }
}

/*
void initialize(void)
{
  for(int n=0;n<255;n++)
  {c[n] = 0;}
}
*/

//ANN 8
void parse_msg(void){

   Serial.print("cTT = ");
   for(int w=0; w<lenGlobal;w=w+1){
      Serial.print(cTT[w]);
   }
   Serial.println();
   
   String var = String(cTT);
   var = String('[') + var + String(']');
   Serial.print("var = ");
   Serial.println(var);
 
    /********************parse on comma*********************************/
  /*******************orig parse****************************
  int index1 = var.indexOf(',',0);
  int index2 = var.indexOf(',',index1+1);
  int index3 = var.indexOf(',',index2+1);
  int index4 = var.indexOf(',',index3+1);
  int index5 = var.indexOf(',',index4+1);
  
  int indexEND = var.indexOf('?');  //will return -1
  Serial.println(indexEND);
  String X_VALUE = var.substring(1,index1); //omit the [
  String Y_VALUE = var.substring(index1+1,index2);
  String A_VALUE = var.substring(index2+1,index3);
  String B_VALUE = var.substring(index3+1,index4);
  String C_VALUE = var.substring(index4+1,index5);


  Serial.println(X_VALUE);
  Serial.println(Y_VALUE);
  Serial.println(C_VALUE);
  int x_value_int = X_VALUE.toInt();
  x_value_int++;
  Serial.println(x_value_int);
  bufToBot[0] = X_VALUE.toInt();
  bufToBot[1] = Y_VALUE.toInt();
  bufToBot[2] = A_VALUE.toInt();
  bufToBot[3] = B_VALUE.toInt();
  //bufToBot[4] = C_VALUE.toInt(); //SEND COUNT TO BOT only goes to 255,then starts again
  ************************end orig parse*****************************/
  
  /****************************new parse*******************************/
  initialIndex = 1;  //IGNORE THIS start initialIndex at 1 b/c python transmits [ .
  kIndex = 0;
  finalIndex = 0;
  while(finalIndex!=-1){
    finalIndex = var.indexOf(',',initialIndex); 
    bufToBot[kIndex] = var.substring(initialIndex,finalIndex).toInt();
    //Serial.println(bufToBot[kIndex]);
    if(finalIndex==-1){
      //Serial.println(bufToBot[kIndex]);
      initialIndex = 0;
      finalIndex = 0;
      kIndex = 0;
      break;}
    initialIndex = finalIndex+1;
    kIndex++;
  }
/*************************end new parse************************************/
  Serial.print("BUFTOBOT = ");
  for(int m=0;m<20;m++){      //NEW
    Serial.print(bufToBot[m]);
    Serial.print(" ");
  }
  Serial.println(); 
    /*********************end parse on comma****************************/  
}

/*********************END FROM OCV_COLORTRACK11_MS_34_3*******************/

//Replace with your network credentials

//ANN 10
const char* ssid = "ssid";
const char* password = "password";                                                                                                  
const char* ssidAP = "ssidAP"; // ars  soft AP
const char* passwordAP = "passwordAP"; //ars softAP


#define PART_BOUNDARY "123456789000000000000987654321"

// This project was tested with the AI Thinker Model, M5STACK PSRAM Model and M5STACK WITHOUT PSRAM
#define CAMERA_MODEL_T_JOURNAL
//#define CAMERA_MODEL_AI_THINKER
//#define CAMERA_MODEL_M5STACK_PSRAM
//#define CAMERA_MODEL_M5STACK_WITHOUT_PSRAM

// Not tested with this model
//#define CAMERA_MODEL_WROVER_KIT

/*#if defined(CAMERA_MODEL_WROVER_KIT)
  #define PWDN_GPIO_NUM    -1
  #define RESET_GPIO_NUM   -1
  #define XCLK_GPIO_NUM    21
  #define SIOD_GPIO_NUM    26
  #define SIOC_GPIO_NUM    27
  
  #define Y9_GPIO_NUM      35
  #define Y8_GPIO_NUM      34
  #define Y7_GPIO_NUM      39
  #define Y6_GPIO_NUM      36
  #define Y5_GPIO_NUM      19
  #define Y4_GPIO_NUM      18
  #define Y3_GPIO_NUM       5
  #define Y2_GPIO_NUM       4
  #define VSYNC_GPIO_NUM   25
  #define HREF_GPIO_NUM    23
  #define PCLK_GPIO_NUM    22

#elif defined(CAMERA_MODEL_M5STACK_PSRAM)
  #define PWDN_GPIO_NUM     -1
  #define RESET_GPIO_NUM    15
  #define XCLK_GPIO_NUM     27
  #define SIOD_GPIO_NUM     25
  #define SIOC_GPIO_NUM     23
  
  #define Y9_GPIO_NUM       19
  #define Y8_GPIO_NUM       36
  #define Y7_GPIO_NUM       18
  #define Y6_GPIO_NUM       39
  #define Y5_GPIO_NUM        5
  #define Y4_GPIO_NUM       34
  #define Y3_GPIO_NUM       35
  #define Y2_GPIO_NUM       32
  #define VSYNC_GPIO_NUM    22
  #define HREF_GPIO_NUM     26
  #define PCLK_GPIO_NUM     21

#elif defined(CAMERA_MODEL_M5STACK_WITHOUT_PSRAM)
  #define PWDN_GPIO_NUM     -1
  #define RESET_GPIO_NUM    15
  #define XCLK_GPIO_NUM     27
  #define SIOD_GPIO_NUM     25
  #define SIOC_GPIO_NUM     23
  
  #define Y9_GPIO_NUM       19
  #define Y8_GPIO_NUM       36
  #define Y7_GPIO_NUM       18
  #define Y6_GPIO_NUM       39
  #define Y5_GPIO_NUM        5
  #define Y4_GPIO_NUM       34
  #define Y3_GPIO_NUM       35
  #define Y2_GPIO_NUM       17
  #define VSYNC_GPIO_NUM    22
  #define HREF_GPIO_NUM     26
  #define PCLK_GPIO_NUM     21

#elif defined(CAMERA_MODEL_AI_THINKER)
  #define PWDN_GPIO_NUM     32
  #define RESET_GPIO_NUM    -1
  #define XCLK_GPIO_NUM      0
  #define SIOD_GPIO_NUM     26
  #define SIOC_GPIO_NUM     27
  
  #define Y9_GPIO_NUM       35
  #define Y8_GPIO_NUM       34
  #define Y7_GPIO_NUM       39
  #define Y6_GPIO_NUM       36
  #define Y5_GPIO_NUM       21
  #define Y4_GPIO_NUM       19
  #define Y3_GPIO_NUM       18
  #define Y2_GPIO_NUM        5
  #define VSYNC_GPIO_NUM    25
  #define HREF_GPIO_NUM     23
  #define PCLK_GPIO_NUM     22
#elif defined(CAMERA_MODEL_T_JOURNAL)*/

//ANN 11
//       T-JOURNAL                     AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM     27     //         0
#define SIOD_GPIO_NUM     25     //        26
#define SIOC_GPIO_NUM     23     //        27
  
#define Y9_GPIO_NUM       19     //        35
#define Y8_GPIO_NUM       36     //        34
#define Y7_GPIO_NUM       18     //        39
#define Y6_GPIO_NUM       39     //        36
#define Y5_GPIO_NUM        5     //        21
#define Y4_GPIO_NUM       34     //        19
#define Y3_GPIO_NUM       35     //        18
#define Y2_GPIO_NUM       17     //         5
#define VSYNC_GPIO_NUM    22     //        25
#define HREF_GPIO_NUM     26     //        23
#define PCLK_GPIO_NUM     21     //        22  
/*#else
  #error "Camera model not selected"
#endif*/

//ANN 12
static const char* _STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char* _STREAM_BOUNDARY = "\r\n--" PART_BOUNDARY "\r\n";
static const char* _STREAM_PART = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

httpd_handle_t stream_httpd = NULL;

static esp_err_t stream_handler(httpd_req_t *req){
  camera_fb_t * fb = NULL;
  esp_err_t res = ESP_OK;
  size_t _jpg_buf_len = 0;
  uint8_t * _jpg_buf = NULL;
  char * part_buf[64];

  res = httpd_resp_set_type(req, _STREAM_CONTENT_TYPE);
  if(res != ESP_OK){
    return res;
  }

  while(true){
    fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Camera capture failed");
      res = ESP_FAIL;
    } else {
      if(fb->width > 400){
        if(fb->format != PIXFORMAT_JPEG){
          bool jpeg_converted = frame2jpg(fb, 80, &_jpg_buf, &_jpg_buf_len);
          esp_camera_fb_return(fb);
          fb = NULL;
          if(!jpeg_converted){
            Serial.println("JPEG compression failed");
            res = ESP_FAIL;
          }
        } else {
          _jpg_buf_len = fb->len;
          _jpg_buf = fb->buf;
        }
      }
    }
    if(res == ESP_OK){
      size_t hlen = snprintf((char *)part_buf, 64, _STREAM_PART, _jpg_buf_len);
      res = httpd_resp_send_chunk(req, (const char *)part_buf, hlen);
    }
    if(res == ESP_OK){
      res = httpd_resp_send_chunk(req, (const char *)_jpg_buf, _jpg_buf_len);
    }
    if(res == ESP_OK){
      res = httpd_resp_send_chunk(req, _STREAM_BOUNDARY, strlen(_STREAM_BOUNDARY));
    }
    if(fb){
      esp_camera_fb_return(fb);
      fb = NULL;
      _jpg_buf = NULL;
    } else if(_jpg_buf){
      free(_jpg_buf);
      _jpg_buf = NULL;
    }
    if(res != ESP_OK){
      break;
    }
    //Serial.printf("MJPG: %uB\n",(uint32_t)(_jpg_buf_len));
  }
  return res;
}

void startCameraServer(){
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  config.server_port = 80;

  httpd_uri_t index_uri = {
    .uri       = "/",
    .method    = HTTP_GET,
    .handler   = stream_handler,
    .user_ctx  = NULL
  };
  
  //Serial.printf("Starting web server on port: '%d'\n", config.server_port);
  if (httpd_start(&stream_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(stream_httpd, &index_uri);
  }
}

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector
 
  Serial.begin(115200);
  Serial.setDebugOutput(false);
  Serial.println();

  myWire.begin(SDA,SCL);
  
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG; 
  
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }
  
  // Camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }
 // Wi-Fi connection

 #if defined(SOFTAP)
/******************SOFTAP**********************************/
  WiFi.softAP(ssidAP,NULL,1,0,1);
  // ssid,pwd,channel(1-13), broadcast/hidden, max connections(4)
  Serial.print("Setting AP..");
  IPAddress ip = WiFi.softAPIP();

  /*
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  */
  Serial.print("softIP = ");
  Serial.println(ip);
  
  Serial.println("");
  Serial.println("WiFi connected");
  
  Serial.print("Camera Stream Ready! Go to: http://");
  //Serial.println(WiFi.localIP()); ars using softAP
  //Serial.println(IP);
/**********************END SOFTAP*******************************/ 

  
 #else
 /***************STATION POINT***********************/
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  Serial.print("Camera Stream Ready! Go to: http://");
  Serial.print(WiFi.localIP());
  IPAddress ip = WiFi.localIP();
   /********************END STATION POINT**************************/

 #endif

  /********************FROM OCV_COLORTRACK11_MS_34_3************/
    /********************transmit ip address******************************/


    //bufIP[0] = ip[0];
  //Serial.println(String(ip[0]));
  String ipString = String(ip[0])+String('.')+String(ip[1])+String('.')+
                      String(ip[2])+String('.')+String(ip[3]);
  Serial.println(ipString);
  int z = String(ip[0]).toInt();                    
  z=z+1;
  Serial.println(z);
  bufIP[0] = (byte)String(ip[0]).toInt();  //bufIP[] is byte array
  Serial.println(bufIP[0]);
  for(int k=0; k<=3; k++){
    //bufIP[k] = (byte)String(ip[k]).toInt();  //bufIP[] is byte array
    bufIP[k] = String(ip[k]).toInt();  //bufIP[] is byte array
  }
  //Serial.println((int)bufIP[2]); 
  Serial.println(bufIP[1]);
  Serial.println(bufIP[2]);
  Serial.println(bufIP[3]);
  
  /***********************end transmit ip address************************************/
  

  ws.onEvent(onWsEvent);
  server3.addHandler(&ws);  
  
  server3.begin(); 
  /********************END FROM OCV_COLORTRACK11_MS_34_3************/
  
  // Start streaming web server
  startCameraServer();
}

//ANN 13
void loop() {
  delay(1);

  /********************FROM OCV_COLORTRACK11_MS_34_3************/
  if(One_Time_Transmit==1){
     delay(4000);
     initializeTT();
     i2cTransmit();
     One_Time_Transmit = 0;
  }
   /********************END FROM OCV_COLORTRACK11_MS_34_3************/
}
