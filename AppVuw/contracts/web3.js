/* eslint-disable */
var Vue = require('vue')
var Web3 = require('web3')

 
// explicit installation required in module environments
// Vue.use(VueWeb3, { web3: new Web3(web3.currentProvider) })

if (window.ethereum) {
  window.web3 = new Web3(ethereum);
  try {
    // Request account access if needed
    ethereum.enable();
  } catch (error) {
    // User denied account access...
  }
} else if (window.web3) {
  // Legacy dapp browsers...
  window.web3 = new Web3(web3.currentProvider);
} else {
  // Non-dapp browsers...
  console.log('Non-Ethereum browser detected. You should consider trying MetaMask!');
}

export default web3;
