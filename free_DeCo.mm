<map version="freeplane 1.12.15">
<!--To view this file, download free mind mapping software Freeplane from https://www.freeplane.org -->
<bookmarks/>
<node FOLDED="false" ID="ID_554549469" CREATED="1768298777867" MODIFIED="1768404383831"><richcontent TYPE="NODE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      <b><span style="font-size: large;">&#xa0;DeCo</span></b>
    </p>
    <p>
      (Device Communication)
    </p>
  </body>
</html>
</richcontent>
<hook NAME="MapStyle" zoom="0.75">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" auto_compact_layout="true" fit_to_viewport="false" show_icons="BESIDE_NODES" show_tags="UNDER_NODES" showTagCategories="false" show_icon_for_attributes="true" show_note_icons="true"/>
    <tags category_separator="::"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ID="ID_271890427" ICON_SIZE="12 pt" COLOR="#000000" STYLE="fork">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="200" DASH="" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_271890427" STARTARROW="NONE" ENDARROW="DEFAULT"/>
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
<richcontent TYPE="DETAILS" CONTENT-TYPE="plain/auto"/>
<richcontent TYPE="NOTE" CONTENT-TYPE="plain/auto"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.tags">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.selection" BACKGROUND_COLOR="#afd3f7" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#afd3f7"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important" ID="ID_67550811">
<icon BUILTIN="yes"/>
<arrowlink COLOR="#003399" TRANSPARENCY="255" DESTINATION="ID_67550811"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.flower" COLOR="#ffffff" BACKGROUND_COLOR="#255aba" STYLE="oval" TEXT_ALIGN="CENTER" BORDER_WIDTH_LIKE_EDGE="false" BORDER_WIDTH="22 pt" BORDER_COLOR_LIKE_EDGE="false" BORDER_COLOR="#f9d71c" BORDER_DASH_LIKE_EDGE="false" BORDER_DASH="CLOSE_DOTS" MAX_WIDTH="6 cm" MIN_WIDTH="3 cm"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="bottom_or_right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10 pt" SHAPE_VERTICAL_MARGIN="10 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<node TEXT="schwebender Knoten" LOCALIZED_STYLE_REF="defaultstyle.floating" POSITION="bottom_or_right" ID="ID_1782138016" CREATED="1768405852767" MODIFIED="1768405916807" HGAP_QUANTITY="77.31544 pt" VSHIFT_QUANTITY="-162.84564 pt">
<hook NAME="FreeNode"/>
</node>
<node TEXT="config.py" POSITION="bottom_or_right" ID="ID_769395070" CREATED="1768298962074" MODIFIED="1768299016457"/>
<node TEXT="device_discovery" POSITION="bottom_or_right" ID="ID_532852364" CREATED="1768299017812" MODIFIED="1768299071110">
<node TEXT="zeroconfig Variante" ID="ID_851766907" CREATED="1768299107005" MODIFIED="1768299133560"/>
<node TEXT="ARP Variante" ID="ID_1823200513" CREATED="1768299134626" MODIFIED="1768299145819"/>
</node>
<node TEXT="Shelly Handler" POSITION="bottom_or_right" ID="ID_930155583" CREATED="1768299150680" MODIFIED="1768405997597">
<node TEXT="class ShellyHandler" ID="ID_727420365" CREATED="1768299317080" MODIFIED="1768405997596" VSHIFT_QUANTITY="-3.86577 pt">
<node TEXT="query_shelly()" ID="ID_1854127970" CREATED="1768299336132" MODIFIED="1768299391319"/>
<node TEXT="_has_rpc()" ID="ID_160912779" CREATED="1768299350630" MODIFIED="1768299401174"/>
<node TEXT="detect_capabilities()" ID="ID_1207238325" CREATED="1768299378652" MODIFIED="1768299384685"/>
<node TEXT="derive_category_from_caps() " ID="ID_282895085" CREATED="1768299413296" MODIFIED="1768299433188"/>
</node>
</node>
<node TEXT="ESP Handler" POSITION="bottom_or_right" ID="ID_106641947" CREATED="1768299185040" MODIFIED="1768299193620">
<node TEXT="class ESPHandler()" ID="ID_364568508" CREATED="1768303258650" MODIFIED="1768303333516">
<node TEXT="query_esp()" ID="ID_1954256760" CREATED="1768303287556" MODIFIED="1768303297080"/>
<node TEXT="(...)" ID="ID_975265095" CREATED="1768303297865" MODIFIED="1768303303810"/>
</node>
</node>
<node TEXT="registry" POSITION="bottom_or_right" ID="ID_1948448603" CREATED="1768299194572" MODIFIED="1768299201830">
<node TEXT="class registry()" ID="ID_28622965" CREATED="1768303355363" MODIFIED="1768303366971">
<node TEXT="update_registry()" ID="ID_1050480188" CREATED="1768303438831" MODIFIED="1768303449254"/>
<node TEXT="load_registry()" ID="ID_265776445" CREATED="1768303383786" MODIFIED="1768303398106"/>
<node TEXT="save_registry()" ID="ID_600328195" CREATED="1768303402906" MODIFIED="1768303416186"/>
</node>
</node>
<node TEXT="NetworkScanner" POSITION="bottom_or_right" ID="ID_1406023398" CREATED="1768303952100" MODIFIED="1768303972004">
<node TEXT="wäre evtl. der einstieg für DeCon von wo aus die Handler-Aufrufe erfolgen (s. Frage 2)" ID="ID_659956308" CREATED="1768303995150" MODIFIED="1768304086122"/>
<node TEXT="discover_ips()" ID="ID_1639865687" CREATED="1768304118273" MODIFIED="1768304138583"/>
<node TEXT="async def identify_device()" ID="ID_650324586" CREATED="1768304139348" MODIFIED="1768304152070"/>
<node TEXT="run_full_scan()" ID="ID_1737756095" CREATED="1768304166448" MODIFIED="1768304176503"/>
</node>
<node TEXT="thread-Gedöns: wer startet die, wo kommen benötigte Infos her etc.?" POSITION="bottom_or_right" ID="ID_616115172" CREATED="1768306882868" MODIFIED="1768306957731"/>
<node POSITION="top_or_left" ID="ID_415938188" CREATED="1768303516928" MODIFIED="1768306842540"><richcontent TYPE="NODE">

<html>
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
