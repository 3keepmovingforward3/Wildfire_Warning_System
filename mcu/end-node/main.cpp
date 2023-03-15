/*
	mcu_receiver_edge_node.cpp
	Written as proof of concept and senior design project
	Used to program a hardware developement board
	Board: Heltec ESP32 WiFi LoRa V2
	Date:FALL2020
	
	Thanks to "ESP32_MailClient" library as found on Github
	At creation, a copy of the used libraries was included.
	
	I've tried to name variables as close to the reason of creation as possible
	I've tried formatting as well as can be.
	I've tried commenting every line that needs extended description
*/

#include <Arduino.h> // allows simple controls, like delay, for debug
#include "heltec.h" // included, wifi and lora esp32 helper library
#include "ESP32_MailClient.h" // smtp email library for system external warning
#include <iostream> // for support during debug
#include <string> // for string compare for simple proof of concept control flow

#define BAND    915E6  //868E6/915E6MHZ, but 915 is for U.S.A., 868 is U.K.

#define emailSenderAccount    "" // shown during proof of concept, personal information
#define emailSenderPassword   "" // ditto, personal information
#define emailRecipient        "" // example email can be entered here
#define smtpServer            "smtp.office365.com" // example smtp server, used in POC
#define smtpServerPort        587 // specific port, includes TLS security
#define emailSubject          "Alarm" // makes reading down in the code easier

// NETWORK CREDENTIALS
// Infrastrucure, during POC, used personal wifi settings
//
const char* ssid = ""; 
const char* password = "";

// The Email Sending data object contains config and data to send
//
SMTPData smtpData;

// Function prototypes
//
void email_setup(void);
void sendCallback(SendStatus);

void setup() {
//WIFI Kit series V1 not support Vext control
//Built in heltec board initialization
Heltec.begin(true /*DisplayEnable Enable*/, true /*Heltec.Heltec.Heltec.LoRa Disable*/, true /*Serial Enable*/, true /*PABOOST Enable*/, BAND /*long BAND*/);

//WiFi connect loop
//Waits forever, leaves on connection
//Falls Through to debug string
WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(200);
  }

  // jump to loop, we're polling lora
  //
  Serial.printf("\nEntering LoRa Polling...");

}

void loop() {
 // try to parse packet
  int packetSize = LoRa.parsePacket(); //object creation, dynamic sizing
  std::string s; //cpp strings have many useful methods, like compare
  std::string t = "ALARM"; //simple compare string for POC
  if (packetSize) {
    // read packet
    while (LoRa.available()) { //read until end signal
      s+=(char) LoRa.read(); //append characters into string
    }
    
    int res = s.compare(t); //string compare method if(true){return 0;}
    Serial.print("compare result: "); //formatting
    Serial.println(res); //probably don't need the newline
    if(res==0){
      Serial.print("\nALARM!"); //debug
      email_setup(); //start email setup
    }
    else {
      Serial.print("Received Something Other than ALARM\n");
      }
  }
    
}

void email_setup(){
  // As given from library, see previous comments for informationn on variables
  // You can think of the object having all the attributes being added at once
  // like a struct
  //
  smtpData.setLogin(smtpServer, smtpServerPort, emailSenderAccount, emailSenderPassword);

  // Don't need to use since we already chose through port selection.
  // For library version 1.2.0 and later which STARTTLS protocol was supported,the STARTTLS will be 
  // enabled automatically when port 587 was used, or enable it manually using setSTARTTLS function.
  //smtpData.setSTARTTLS(true);

  // Set the sender name and Email
  // Metadata
  //
  smtpData.setSender("ESP32", emailSenderAccount);

  // Set Email priority or importance High, Normal, Low or 1 to 5 (1 is highest)
  // Old api, but might still be used by full email client
  //
  smtpData.setPriority("High");

  // Set the subject
  // true = rich-text/ false = plain-txt
  // for compatibily, pick plain-txt
  smtpData.setSubject(emailSubject);
  smtpData.setMessage("ALARM!!!", false);

  // Add recipients, you can add more than one recipient by
  // calling the follwing command a multiple times, with new email addreass strings
  smtpData.addRecipient(emailRecipient);
  
  // Sets functions we'll be passing from above as an object, which is the one we just created.
  //
  smtpData.setSendCallback(sendCallback);

    //Start sending Email, can be set callback function to track the status
  if (!MailClient.sendMail(smtpData))
    Serial.println("Error sending Email, " + MailClient.smtpErrorReason());

  //Clear all data from Email object to free memory
  smtpData.empty();
}

// Callback function to get the Email sending status
void sendCallback(SendStatus msg) {
  // Print the current status
  Serial.println(msg.info());

  // Do something when complete
  if (msg.success()) {
    Serial.println("----------------");
  }
}
