const env = process.env; 
var express = require('express'); 
const mongoose = require("mongoose"); 
const crypto = require("crypto");

const Users = require("../../models/Users.js");
const senderAddress= env.BLOCKCHAIN_SENDER_ADDRESS || "0x23b0438547a478A4a32501961137Dd0E1E8C36FE";
const senderPrivateKey= env.BLOCKCHAIN_SENDER_PRIVATE_KEY || "0x411dfacefaff8672907b8c0163485422cdc9d63b80f5414825ecc2dadab7f11e";
var router = express.Router();

// Function to derive a 256-bit key from the OTP using PBKDF2
function deriveAesKeyFromOTP(otp, salt) {
  const iterations = 100000;
  const keyLength = 32; // 256 bits
  const digest = 'sha256';

  return crypto.pbkdf2Sync(otp, salt, iterations, keyLength, digest);
}

// Function to encrypt a message using OTP
function encryptMessage(message, otp) {
  const iv = crypto.randomBytes(16); // Generate a random Initialization Vector (IV)
  const salt = crypto.randomBytes(16); // Generate a random salt

  const aesKey = deriveAesKeyFromOTP(otp, salt);
  const cipher = crypto.createCipheriv('aes-256-cbc', aesKey, iv);

  let encrypted = cipher.update(message, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  return `${salt.toString('hex')}:${iv.toString('hex')}:${encrypted}`;
}


// Function used to generate random OTP
function generateRandomOTP(length) {
  const characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  let result = "";
  for (let i = 0; i < length; i++) {
    const randomIndex = crypto.randomInt(0,characters.length);
    result += characters.charAt(randomIndex);
  }
  return result;
}

// Used to log a user in
router.post("/login", async (req,res) =>{
  var {uid} = req.body;
  if(uid == null) {
    out = {
      status:"err_incomplete_request",
      description:"Request is incomplete, username not provided"
    }
    res.status(400).json(out);
    return;
  }
  try {
    // Checking if the user id is registered
    var user = await Users.find({uid:uid});
    if(user.length < 1) {
      // User doesnt registered
      out = {
        status:"err_not_registered",
        description:"The user was not registered "
      }
      res.status(409).json(out)
      return
    }else {
      // the user was registered 
      user = user[0];
      var otp = generateRandomOTP(6);
      console.log("OTP Send : "+otp)
      var msg = encryptMessage(user.key,otp);
      if(user.completed_registration) {
        // The user registration was not completed 
        // i.e the user may not be entered to the blockchain 
        out = {
          status:"success_not_completed_registration",
          description:"The registration may not be completed",
          content: {
            key: msg
          }
        }
        res.status(200).json(out);
        return;
      }else {
        // The user registration is completed
        out = {
          status:"success",
          description:"Credentials send",
          content:{
            key:msg,
            approved_to_vote: user.approved
          }
        }
        res.status(200).json(out);
        return;
      }
    }
  }catch (err) {
    console.log("Unexpected error");
    console.log(err);
    out = {
      status:"err_unexpected",
      description:"An Unexpected error occured"
    }
    res.status(500).json(out);
    return;
  }
});

// Used to register a user to the server
router.post('/register', async (req,res) => {
  var {address, key,uid} = req.body;
  if(address == null || key == null || uid == null) {
    // The request is not complete
    out = {
      status:"err_incomplete_request",
      description:"The request is incomplete, ("+(address == null ? "address, " : "")+(key == null ? "key, ":"")+(uid == null ? "uid":"")+" not given)"
    }
    res.status(400).json(out);
    return;
  }
  console.log("Request from : "+uid+" : "+address+" : password("+key+")");
  var out = {};
  try{
    // Check if an account was already created or not
    var user = await Users.find({uid:uid});
    if (user.length > 0) {
      // User already registered
      user = user[0];
      out = {
        status:"err_already_registered",
        description: "The userId is invalid. The userId is already registered!"
      }
      res.status(409).json(out); // send
      return;
    }else {
      // Check if the address is allocated for any other user 
      var user = await Users.find({address:address});
      if(user.length > 0) {
        out = {
          status:"err_address_used",
          description:"The address is already allocated for a user, choose another one"
        }
        res.status(409).json(out); // send
        return;
      }else {
        // The request is ok, do the registration
        var user = Users({
          uid:uid,
          address:address,
          key:key
        });
        await user.save();
        console.log("Registered: "+uid+" : "+address);
        out = {
          status:"success",
          description:"Successfully Completed Registration",
          content:{
            address:address
          }
        }
        res.status(200).json(out);
        return;
      }
    }
  }catch(err) {
    console.log(err);
    out = {
      status:"err_unexpected",
      description: "An Unexpected error occured!"
    }
    res.status(500).json(out); // send
    return;
  }
});

// Allocated ethers for Registration purpose 
router.post('/allocateEthersForRegistration',async (req,res) => {
  var {address} = req.body;
  var {web3} = req;
  var out = {};
  if(address == null) res.status(400).json({status:"err_incomplete_request",description:"Incomplete request, Address not given"});
  else {
    try{
      console.log(`Attempting to make transaction from ${senderAddress} to ${address}`);
      const nonce = await web3.eth.getTransactionCount(senderAddress);

      // Prepare the transaction object
      const txObject = {
        nonce: nonce,
        from:senderAddress,
        to: address,
        value: web3.utils.toWei("0.0005", "ether"),
        // gasLimit: web3.utils.toHex(21000),
        // gasPrice: await web3.eth.getGasPrice(),
        maxFeePerGas: web3.utils.toHex(999999999999),
        maxPriorityFeePerGas: web3.utils.toHex(2500)
      };
      txObject.gas = await web3.eth.estimateGas(txObject);
      console.log(txObject);
      
      await web3.eth.accounts.wallet.add(senderPrivateKey);
      const createReceipt = await web3.eth.sendTransaction(txObject);
      // console.log(createReceipt)
      res.json({ status: "success",
        content:{receipt: createReceipt.transactionHash }});
    }catch(err) {
      console.log("Unexpected error occured");
      console.log(err);
      res.status(500).json({
        status:"err_unexpected",
        decription:"An Unexpected error occured"
      });
    }

  }
});

module.exports = router