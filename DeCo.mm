<map version="1.0.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1768298777867" ID="ID_554549469" MODIFIED="1768306872943">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      <font size="5"><b>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;DeCo</b></font>
    </p>
    <p>
      (Device Communication)
    </p>
  </body>
</html></richcontent>
<node CREATED="1768298962074" ID="ID_769395070" MODIFIED="1768299016457" POSITION="right" TEXT="config.py"/>
<node CREATED="1768299017812" ID="ID_532852364" MODIFIED="1768299071110" POSITION="right" TEXT="device_discovery">
<node CREATED="1768299107005" ID="ID_851766907" MODIFIED="1768299133560" TEXT="zeroconfig Variante"/>
<node CREATED="1768299134626" ID="ID_1823200513" MODIFIED="1768299145819" TEXT="ARP Variante"/>
</node>
<node CREATED="1768299150680" ID="ID_930155583" MODIFIED="1768299516842" POSITION="right" TEXT="Shelly Handler">
<node CREATED="1768299317080" ID="ID_727420365" MODIFIED="1768303343782" TEXT="class ShellyHandler">
<node CREATED="1768299336132" ID="ID_1854127970" MODIFIED="1768299391319" TEXT="query_shelly()"/>
<node CREATED="1768299350630" ID="ID_160912779" MODIFIED="1768299401174" TEXT="_has_rpc()"/>
<node CREATED="1768299378652" ID="ID_1207238325" MODIFIED="1768299384685" TEXT="detect_capabilities()"/>
<node CREATED="1768299413296" ID="ID_282895085" MODIFIED="1768299433188" TEXT="derive_category_from_caps() "/>
</node>
</node>
<node CREATED="1768299185040" ID="ID_106641947" MODIFIED="1768299193620" POSITION="right" TEXT="ESP Handler">
<node CREATED="1768303258650" ID="ID_364568508" MODIFIED="1768303333516" TEXT="class ESPHandler()">
<node CREATED="1768303287556" ID="ID_1954256760" MODIFIED="1768303297080" TEXT="query_esp()"/>
<node CREATED="1768303297865" ID="ID_975265095" MODIFIED="1768303303810" TEXT="(...)"/>
</node>
</node>
<node CREATED="1768299194572" ID="ID_1948448603" MODIFIED="1768299201830" POSITION="right" TEXT="registry">
<node CREATED="1768303355363" ID="ID_28622965" MODIFIED="1768303366971" TEXT="class registry()">
<node CREATED="1768303438831" ID="ID_1050480188" MODIFIED="1768303449254" TEXT="update_registry()"/>
<node CREATED="1768303383786" ID="ID_265776445" MODIFIED="1768303398106" TEXT="load_registry()"/>
<node CREATED="1768303402906" ID="ID_600328195" MODIFIED="1768303416186" TEXT="save_registry()"/>
</node>
</node>
<node CREATED="1768303952100" ID="ID_1406023398" MODIFIED="1768303972004" POSITION="right" TEXT="NetworkScanner">
<node CREATED="1768303995150" ID="ID_659956308" MODIFIED="1768304086122" TEXT="w&#xe4;re evtl. der einstieg f&#xfc;r DeCon von wo aus die Handler-Aufrufe erfolgen (s. Frage 2)"/>
<node CREATED="1768304118273" ID="ID_1639865687" MODIFIED="1768304138583" TEXT="discover_ips()"/>
<node CREATED="1768304139348" ID="ID_650324586" MODIFIED="1768304152070" TEXT="async def identify_device()"/>
<node CREATED="1768304166448" ID="ID_1737756095" MODIFIED="1768304176503" TEXT="run_full_scan()"/>
</node>
<node CREATED="1768306882868" ID="ID_616115172" MODIFIED="1768306957731" POSITION="right" TEXT="thread-Ged&#xf6;ns: wer startet die, wo kommen ben&#xf6;tigte Infos her etc.?"/>
<node CREATED="1768303516928" ID="ID_415938188" MODIFIED="1768306842540" POSITION="left">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Fragen:
    </p>
    <ul>
      <li>
        k&#246;nnen Shelly-Handler und ESP-Handler zusammen gelgt werden? NEIN
      </li>
      <li>
        so kapseln das DeCo gar nicht merkt das verschieden Handler am Werke sind?
      </li>
      <li>
        was soll die Registry eigentlich genau enthalten
      </li>
      <li>
        soll noch eine Ger&#228;te-YML angelggt werden
      </li>
    </ul>
  </body>
</html>
</richcontent>
</node>
</node>
</map>
