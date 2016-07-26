import unittest
import wlrutil
import LabelledImage
import numpy as np

class LabelledImageTests( unittest.TestCase ) :

    def testCreate( self ) :
        labelledImage = LabelledImage.LabelledImage( 32, 41, 7 )
        self.assertEqual( 32, labelledImage.rows )
        self.assertEqual( 41, labelledImage.columns )
        self.assertEqual( 7, labelledImage.label )

    def testDrawRow( self ) :
        labelledImage = LabelledImage.LabelledImage( 32, 41, 7 )
        labelledImage.DrawRow( 20 )
        labelledImage.DrawColumn( 5 )
        ### labelledImage.Display()

    def testIsEqual( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li2 = LabelledImage.LabelledImage( 32, 41, 7 )
        self.assertEqual( True, li1.IsEqual( li2 ) )

    def testLabelsNotEqual( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li2 = LabelledImage.LabelledImage( 32, 41, 8 )
        self.assertEqual( False, li1.IsEqual( li2 ) )

    def testRowsNotEqual( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li2 = LabelledImage.LabelledImage( 35, 41, 7 )
        self.assertEqual( False, li1.IsEqual( li2 ) )

    def testColumnsNotEqual( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li2 = LabelledImage.LabelledImage( 32, 45, 7 )
        self.assertEqual( False, li1.IsEqual( li2 ) )

    def testContentNotEqual( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li2 = LabelledImage.LabelledImage( 32, 41, 7 )
        li2.DrawRow( 20 )
        self.assertEqual( False, li1.IsEqual( li2 ) )

    def testDatumRoundTrip( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li1.DrawRow(20)
        li1.DrawColumn(5)
        datum = wlrutil.LabelledImageToDatum( li1 )
        li2 = wlrutil.DatumToLabelledImage( datum )
        self.assertEqual( True, li1.IsEqual( li2 ) )

    def testValueRoundTrip( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li1.DrawRow(20)
        li1.DrawColumn(5)
        value = wlrutil.LabelledImageToLevelDBValue( li1 )
        li2 = wlrutil.LevelDBValueToLabelledImage( value )
        print "testValueRoundTrip"
        self.assertEqual( True, li1.IsEqual( li2 ) )

    def testValueToDatumRoundTrip ( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li1.DrawRow(20)
        li1.DrawColumn(5)
        value1 = wlrutil.LabelledImageToLevelDBValue( li1 )
        datum = wlrutil.LevelDBValueToDatum( value1 )
        value2 = wlrutil.DatumToLevelDBValue( datum )
        self.assertEqual( True, wlrutil.IsEqualLevelDBValues( value1, value2 ) )

    def testValueNotEqualRows( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        value1 = wlrutil.LabelledImageToLevelDBValue( li1 )
        li2 = LabelledImage.LabelledImage( 35, 41, 7 )
        value2 = wlrutil.LabelledImageToLevelDBValue( li2 )
        self.assertEqual( False, wlrutil.IsEqualLevelDBValues( value1, value2 ) )

    def testValueNotEqualColumns( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        value1 = wlrutil.LabelledImageToLevelDBValue( li1 )
        li2 = LabelledImage.LabelledImage( 32, 45, 7 )
        value2 = wlrutil.LabelledImageToLevelDBValue( li2 )
        self.assertEqual( False, wlrutil.IsEqualLevelDBValues( value1, value2 ) )

    def testValueNotEqualLabels( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        value1 = wlrutil.LabelledImageToLevelDBValue( li1 )
        li2 = LabelledImage.LabelledImage( 32, 41, 9 )
        value2 = wlrutil.LabelledImageToLevelDBValue( li2 )
        self.assertEqual( False, wlrutil.IsEqualLevelDBValues( value1, value2 ) )

    def testValueNotEqualImage( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        li1.DrawRow( 20 )
        value1 = wlrutil.LabelledImageToLevelDBValue( li1 )
        li2 = LabelledImage.LabelledImage( 32, 41, 7 )
        value2 = wlrutil.LabelledImageToLevelDBValue( li2 )
        self.assertEqual( False, wlrutil.IsEqualLevelDBValues( value1, value2 ) )

    def testValueEqual( self ) :
        li1 = LabelledImage.LabelledImage( 32, 41, 7 )
        value1 = wlrutil.LabelledImageToLevelDBValue( li1 )
        li2 = LabelledImage.LabelledImage( 32, 41, 7 )
        value2 = wlrutil.LabelledImageToLevelDBValue( li2 )
        self.assertEqual( True, wlrutil.IsEqualLevelDBValues( value1, value2 ) )




if __name__ == '__main__':
    unittest.main()
