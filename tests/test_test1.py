import pytest
import Main

data = "This movie directed by Spilberg is length bus it is good."

def test_hk():
    t, tt = Main.Chunk_Data(data)
	assert t is not None