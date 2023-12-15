const env = process.env;

const web3 = require("web3");
const express = require("express");
const app = express();
var cors = require('cors');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const Tx = require('ethereumjs-tx').Transaction;
var mongoose = require("mongoose");

const senderAddress= env.BLOCKCHAIN_SENDER_ADDRESS || "0x23b0438547a478A4a32501961137Dd0E1E8C36FE";
const senderPrivateKey= env.BLOCKCHAIN_SENDER_PRIVATE_KEY || "0x411dfacefaff8672907b8c0163485422cdc9d63b80f5414825ecc2dadab7f11e";

const publicRouter = require("./routes/api/public.js");

app.use(cors());
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(function(req, res, next) {
  res.header('Access-Control-Allow-Credentials', true);
  res.header('Access-Control-Allow-Origin', req.headers.origin);
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,UPDATE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept');
  next();
});
app.use((req,res,next) => {
  web3Provider = new web3.Web3.providers.HttpProvider(env.BLOCKCHAIN_URL || 'http://192.168.18.2:7545');
  req.web3 = new web3.Web3(web3Provider);
  req.senderAccount = {
    privateKey: Buffer.from(senderPrivateKey, 'hex'),
    address: senderAddress
  };
  next();
});

app.use("/api/public/", publicRouter);

const uri = env.DB_URL; 
 mongoose.connect(uri,{ useNewUrlParser: true, useUnifiedTopology: true}) 
   .then((result) =>{ 
     console.log("CONNECTED TO DB"); 
   }) 
   .catch((err) => { 
     console.log("CANT CONNECT TO DB"); 
     console.log(err); 
 }); 
 
app.listen(env.PORT || 3131,()=>{
  console.log("Server started !");
})