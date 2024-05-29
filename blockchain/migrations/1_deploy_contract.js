var CAKEContract = artifacts.require("CAKEContract");

module.exports = function(deployer) {
    deployer.deploy(CAKEContract);
};