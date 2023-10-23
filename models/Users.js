const mongoose = require("mongoose"); 
const Schema = mongoose.Schema; 
  
const schema = new Schema({
  uid:{
    type:String,
    required:true
  },
  address:{
    type:String,
    required:true
  },
  key:{
    type:String,
    required:true
  },
  completed_registration:{
    type:Boolean,
    default:false
  },
  approved:{
    type:Boolean,
    default:false
  }
});

const item = mongoose.model("users",schema);

module.exports = item;