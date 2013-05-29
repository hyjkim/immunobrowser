// First test

module("isPhoneNumber");
test ("Wrong number", function() {
  equal(isPhoneNumber("abcdefg"), false, "All alphabet");
  equal(isPhoneNumber("123456789"), true, "input = 123456789");
});

module("checkChildren");
test("Checks children checkboxes", function () {
  equal(checkChildren(), false, "false is false");
});

isPhoneNumber = function(input) {
  reg = /^\d+$/;
  if (reg.test(input)) {
    return true;
  }
  return false;
}


