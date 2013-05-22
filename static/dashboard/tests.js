// First test

module("isPhoneNumber");
test ("Wrong number", function() {
  equal(isPhoneNumber("abcdefg"), false, "All alphabet");
});
