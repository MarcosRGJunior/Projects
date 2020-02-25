const officegen = require("officegen");
const fs = require("fs");
const os = require("os");
const cmd = require("node-cmd");
const activedirectory = require('activedirectory');

let docx = officegen("docx");


const sAMAccountName = os.userInfo().username;

/*var config = { url: 'ldap://LST-Domain.local',
               baseDN: 'dc=LST-Domain,dc=local', //?
               username: 'adm.marcos.junior@LST-Domain.local',
               password: 'password' }
var ad =  new ActiveDirectory(config);*/


docx.on("finalize", function(written) {
  console.log("Finish to Write a Listo Documment");
});

docx.on("error", function(err) {
  console.log(err);
});

// Find user by a sAMAccountName
/*ad.findUser(sAMAccountName, function(err, user) {
  if (err) {
    console.log('ERROR: ' +JSON.stringify(err));
    return;
  }
 
  if (! user) console.log('User: ' + sAMAccountName + ' not found.');
  else console.log(JSON.stringify(user));
});*/

let writ = docx.createP({ align: "center" });

writ.addText("Example of a Possible Term of Responsibility", {
  font_size: 34,
  bold: true,
  underline: true
});


writ = docx.createP();
writ = docx.createP({ align: "left" });

writ.addText(
  "Taking the Advice from Rafael, I decided to make this docunent in english. "
);

writ.addText(
  "This document is an example of how might work an automatization of the work. "
);

writ.addText("It can tell the username of the employee: ");

writ.addText(os.userInfo().username, { bold: true, underline: true });

writ.addText(". ");

writ.addText(" And can tell the hostname of the PC being used: ");

writ.addText(os.hostname(), { bold: true, underline: true });

writ.addText(". ");

writ.addText(
  "I tried to put out the Serial Number of the PC, but for some reason every time got the value; "
);

 cmd.get("wmic bios get serialnumber", function(err, data, stderr) {
   if (err) {
     console.log(err, stderr);
     return;
   }

  console.log("the Serial Number that is in current use: ", data);
  writeEverything(data)

});

/*
cmd.run("type documentListo.docx>LPT1");
 */

 const writeEverything = (data) => {   //como o node é assincrono o comando não terminava até o o final do programa!!! 
  writ.addText(
    data.trim(), {  //trim diminui o tamanho gerado e a função correta é data.toString()
    bold: true,
    underline: true
  });
  
  writ.addText(". ");
  
  writ.addText(
    "Maybe you could see the printer going automatically to make for it "
  );
  
  writ.addText("For now, i'll fill this with some good phrases of movies: ");
  
  writ.addText(
    "The path of the righteous man is beset on all sides by the inequities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity and good will, shepherds the weak through the valley of the darkness. For he is truly his brother's keeper and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger those who attempt to poison and destroy my brothers. And you will know I am the Lord when I lay my vengeance upon you. "
  );
  
  writ.addText(" To finish: I solemnly swear that i am up to no good.");
  
  writ = docx.createP();
  writ = docx.createP();
  writ = docx.createP();
  writ = docx.createP({ align: "center" });
  
  writ.addText("________________________________________________");
  writ = docx.createP({ align: "left" });
  writ.addText("    Name:", { italic: true, font_size: 10 });
  
  let out = fs.createWriteStream("documentListo.docx");
  
  out.on("error", function(err) {
    console.log(err);
  });
  
  docx.generate(out); // put the text created in de programm.
 }