function doPost(e) {
  var parsedData = parseArduinoData(e);
  writeToSpreadsheet(parsedData);
}

function parseArduinoData(event) {
  var rawData = event.postData.contents;
  var cloudData = JSON.parse(rawData);
  var data = {};

  for (var i = 0; i < cloudData.values.length; i++) {
    data[cloudData.values[i].name] = cloudData.values[i].value;
    data["updateTime"] = cloudData.values[i].updated_at;
  }
  return data;
}

function writeToSpreadsheet(data) {
  var sheet = SpreadsheetApp.getActiveSheet();
  var rowValues = [];  
  sheet.appendRow([data.updateTime, data.moisture, data.temperature]);
}

