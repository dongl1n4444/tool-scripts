#target photoshop
app.bringToFront();

var sizeList =
[
  {"name": "iTunesArtwork",           "size":512},
  {"name": "iTunesArtwork@2x",        "size":1024},
  {"name": "Icon",                    "size":57},
  {"name": "Icon@2x",                 "size":114},
  {"name": "Icon-@2x",                "size":114},
  {"name": "Icon-40",                 "size":40},
  {"name": "Icon-72",                 "size":72},
  {"name": "Icon-72@2x",              "size":144},
  {"name": "Icon-Small",              "size":29},
  {"name": "Icon-Small@2x",           "size":58},
  {"name": "Icon-Small-50",           "size":50},
  {"name": "Icon-Small-50@2x",        "size":100},
  {"name": "Icon-50",                 "size":50},
  {"name": "Icon-57",                 "size":57},
  {"name": "Icon-58",                 "size":58},
  {"name": "Icon-72",                 "size":72},
  {"name": "Icon-76",                 "size":76},
  {"name": "Icon-80",                 "size":80},
  {"name": "Icon-100",                "size":100},
  {"name": "Icon-120",                "size":120},
  {"name": "Icon-144",                "size":144},
  {"name": "Icon-152",                "size":152},
  {"name": "Icon-29",                 "size":29},
  {"name": "Icon-29@2x",              "size":58},
  {"name": "Icon-29@3x",              "size":87},
  {"name": "Icon-40@2x",              "size":80},
  {"name": "Icon-40@3x",              "size":120},
  {"name": "Icon-60@3x",              "size":180},
  {"name": "Icon-60@2x",              "size":120},
  {"name": "Icon-76",                 "size":76},
  {"name": "Icon-76@2x",              "size":152},
  {"name": "Icon-48",              "size":48},
  {"name": "Icon-60",              "size":60},
  {"name": "Icon-96",              "size":96},
  {"name": "Icon-192",              "size":192},
  {"name": "Icon-1024",              "size":1024},
  {"name": "Icon-512",              "size":512},
  {"name": "Icon-36",              "size":36},
];
//尺寸集合
// var sizeList = [1024,512,192,180,152,144,128,120,114,100,96,87,80,76,75,72,66,60,58,57,50,48,44,40,36,32,29,16];

//任意一个宽与高相等的图像，尺寸大于1024x1024像素。
//var fileRef = File.openDialog ("请选择一个文件", "*.png", false);
if (documents.length > 0) {
    var fileRef = activeDocument

    //也可以在这里直接定义一个输出文件夹，Folder.selectDialog("然后选择一个输出文件夹");
    //我这里直接使用被选择图片的相同目录
    var outputFolder = fileRef.parent;

    //打开文件
    // var activeDocument = app.open(fileRef);

    var destFolder = Folder.selectDialog( "请选择一个输出的文件夹：");
    //运行批处理尺寸
    runNow(activeDocument, destFolder) ;
} else {
    alert("请先打开一个1024x1024_png文件");
}

function runNow(activeDocument, destFolder)
{
     if(activeDocument.height != activeDocument.width)
     {
         alert("当前文件宽高尺寸不一致，脚本已中止。");
         return;
     }

    //  if(activeDocument.height < 1024)
    //  {
    //      alert("选择的原始图像尺寸必须大于等于1024x1024像素。");
    //      return;
    //   }


     for(var i = 0; i < sizeList.length; i ++)
     {
         //重置图像尺寸
         activeDocument.resizeImage(UnitValue(sizeList[i].size,"px"),UnitValue(sizeList[i].size,"px"),null,ResampleMethod.BICUBIC);

         //图像无论是放大还是缩小，都会变模糊，只是放大时模糊的快一些，缩小时模糊的慢一些
         //所以这里复制一个图像进行锐化，可以让缩小后的图像清晰一点。
         var duplicateLayer = activeDocument.activeLayer.duplicate();

         activeDocument.activeLayer = duplicateLayer;

         duplicateLayer.applySharpen();//应用锐化
         duplicateLayer.opacity = 40;

         activeDocument.flatten();//合并图层


         var destFileName = destFolder + "/" + sizeList[i].name +".png";

          if (sizeList[i].name == "iTunesArtwork" || sizeList[i].name == "iTunesArtwork@2x")
              destFileName = destFolder + "/" + sizeList[i].name;

         //保存的文件
         var saveFile = new File(destFileName);

         //如果文件已经存在就先删除它
          if (saveFile.exists)
          {
                saveFile.remove();
          }

         //以PNG格式保存，带压缩
         var pngSaveOptions = new ExportOptionsSaveForWeb();
         pngSaveOptions.format = SaveDocumentType.PNG;
         pngSaveOptions.transparency = true;
         pngSaveOptions.includeProfile = false ;
         pngSaveOptions.interlaced = false ;
         pngSaveOptions.PNG8= false ;

         activeDocument.exportDocument(saveFile, ExportType.SAVEFORWEB, pngSaveOptions);

         activeDocument.activeHistoryState = activeDocument.historyStates[0];//还原到打开状态
     }
     activeDocument.close(SaveOptions.DONOTSAVECHANGES);//原始被打开的文件不保存，关闭源文件
}