//////////設定部分//////////

//出力データと実行回数の情報の削除
var reset = false;　//true:削除する false:削除しない　(基本はfalseに設定)

//各言語のファイルの頭文字
const LangAlphabets = ['E', 'C', 'F', 'S', 'G', 'SW', 'K', 'IN', 'A', 'R', 'H', 'I', 'P', 'J'];

//////////////////////////


var properties = PropertiesService.getScriptProperties();　
//PropertiesService.getScriptProperties 関数で、Propertiesクラスのインスタンスを取得する。
//関数を変えることで、データのスコープを変更することができる
//var properties = PropertiesService.getUserProperties();
//var properties = PropertiesService.getDocumentProperties();

//前回のプログラムの実行回数の読み込み(1回目の場合は0を返す)
function loadCount() {
  var count = properties.getProperty("Count");
  if (!count) return 0;
  return parseInt(count, 10);
}

//プログラムの実行回数の保存
function saveCount(count) {
  properties.setProperty("Count", count);
}

//プログラムの実行回数の削除
function deleteCount() {
  properties.deleteProperty("Count");
}

//ファイル読み込み
function getFile(filename) {
  var files = DriveApp.getFilesByName(filename);
  if(!files.hasNext()) {return undefined;}
  return files.next();
}

//メインの関数

function main() {

//Language_AnalysisのSheetを取得
var Language_Analysis = SpreadsheetApp.getActiveSpreadsheet();
var Language_Analysis_Sheet = Language_Analysis.getSheetByName('Sheet1');

//プログラムの実行回数の定義と保存
var countnumber = loadCount() + 1;
saveCount(countnumber);

// Language_Analysisの行番号の定義
var rownumber; 
rownumber = countnumber + 1;

//出力データと実行回数の情報の削除
if(reset) {

  deleteCount();
  console.log('Reset Program Execution Number');

  Language_Analysis_Sheet.getRange(2, 1, rownumber - 1, LangAlphabets.length + 1).clearContent();
  console.log('Clear All Data');

  return;

} else {
}

//実行時の日時を出力
var date = new Date();
var ddate = Utilities.formatDate( date, 'JST', "yyyy/MM/dd:(E) HH'h'mm'm'ss's'");
Language_Analysis_Sheet.getRange(rownumber, 1).setValue(ddate); //実行時の日時をLanguage_Analysisに出力

  // 各言語ファイルの行数をLanguage_Analysisに出力
  for (let step = 0; step < LangAlphabets.length; step++) {
    
    //各言語のファイル名
    var name = LangAlphabets[step] + "Words";

    //各言語ファイルのSheetを取得
    var file = getFile(name);
    var Loopspreadsheet = SpreadsheetApp.open(file);
    var Loopsheet = Loopspreadsheet.getSheetByName('Sheet1');
    
    const LoopValues = Loopsheet.getRange('A:A').getValues();　 //各言語ファイルのA列の値を全て取得
    const LastRow = LoopValues.filter(String).length;　　//空白の要素を除いた長さを取得

    Language_Analysis_Sheet.getRange(rownumber, step + 2).setValue(LastRow); // 各言語ファイルの行数をLanguage_Analysisに出力
    console.log('#%d: %s %d lines', step + 1, name, LastRow); //consoleにも結果を一応出力

  }

console.log('Program Execution Number: %d',countnumber);//プログラムの実行回数出力
console.log('Output Row Number: %d',rownumber); //Language_Analysisの行番号出力
console.log('Date: %s',ddate); //実行時の日時をconsoleに出力


}
