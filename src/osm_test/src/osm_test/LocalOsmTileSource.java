package osm_test;
import org.openstreetmap.gui.jmapviewer.tilesources.AbstractOsmTileSource;

public class LocalOsmTileSource {
    
    public static class LocalMap extends AbstractOsmTileSource {

        private static final String PATTERN = "file:///E:/Maperitive-latest/Maperitive/Tiles";

        private static final String[] SERVER = {"a", "b", "c"};

        private int serverNum;

        public LocalMap() {
            super("LocalOsmMap", PATTERN, "LocalOsmMap");
        }

        @Override
        public String getBaseUrl() {
            String url = String.format(this.baseUrl, new Object[] {SERVER[serverNum]});
            serverNum = (serverNum + 1) % SERVER.length;
            return url;
        }

        @Override
        public int getMaxZoom() {
            return 18;
        }
    }
}

