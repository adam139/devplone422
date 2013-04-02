#-*- coding: UTF-8 -*-
from Products.CMFCore.utils import getToolByName
from eisoo.market.testing import EISOO_MARKET_FUNCTIONAL_TESTING 
from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest

class TestMarketProviewView(unittest.TestCase):
    
    layer = EISOO_MARKET_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        import random
 #       portal.invokeFactory('eisoo.operation.areamanaged', 'areamanaged1')
        portal.invokeFactory('eisoo.operation.areafolder', 'areafolder1')
        portal['areafolder1'].invokeFactory('eisoo.operation.area', 'area1',
                                            name='area1',
                                            level="1",
                                            total_fee = 1000.0,
                                            spent_fee = 500.0,
                                            total_spread_fee = 100.0,
                                            spent_spread_fee = 50.0,
                                            responsible_person=TEST_USER_ID,)                        
        #管辖区域的id,name和被管辖区域的name保持一致
        portal.invokeFactory('eisoo.operation.areamanaged', 'area1',
                             name="area1",)
        
        portal['area1'].invokeFactory('eisoo.operation.channel', 'channel')
        #建立部門
        portal.invokeFactory('eisoo.market.marketfolder', 'marketfolder1')
        
        portal['marketfolder1'].invokeFactory('eisoo.market.departmentfolder', 'departmentfolder1',
                                              name=u"departmentfolder1",)
        
        portal['marketfolder1']['departmentfolder1'].invokeFactory('eisoo.market.department', 'department1',
                                                           dname=u"3",
                                                           number=random.randint(10000000, 100000000),
                                                           total_fee=15213,
                                                           spent_fee=213,
                                                          )
        portal['marketfolder1'].invokeFactory('eisoo.market.giftfolder', 'giftfolder1',
                                              name=u"giftfoler1",)
        portal['marketfolder1']['giftfolder1'].invokeFactory('eisoo.market.gift', 'gift1',
                                                                 name=u"gift1",
                                                                 price=100.0,
                                                                 stock=20,
                                                                 memo=u"h阿",
                                                                 state=1,
                                                                 number=9,

                                                                 )

        portal['marketfolder1'].invokeFactory('eisoo.market.giftapplyfolder', 'giftapplyfolder1')
        

        portal['marketfolder1']['giftapplyfolder1'].invokeFactory('eisoo.market.giftapply', 'giftapply1',
                                                                 name=u"gift1",
                                                                 price=100.0,
                                                                 num=1,
                                                                 next_reviewer=(TEST_USER_ID,),
                                                                 next_obj= -5,
                                                                 number=3,
                                                                 )        
        portal['marketfolder1'].invokeFactory('eisoo.market.promotionapplyfolder', 'promotionapplyfolder1')
        portal['marketfolder1'].invokeFactory('eisoo.market.promotionfolder', 'promotionfolder1')
        
        portal['marketfolder1']['promotionfolder1'].invokeFactory('eisoo.market.promotion', 'promotion1',
                                                                  name=u"promotion1",
                                                                  number=random.randint(10000000, 100000000),
                                                                )
        portal['marketfolder1']['promotionapplyfolder1'].invokeFactory('eisoo.market.promotionapply', 'promotionapply1',
                                                                       name=u"promotion1",
                                                                       next_reviewer=(TEST_USER_ID,),
                                                                       price=100,
                                                                       next_obj= -5,
                                                                       number=3,
                                                                        )   
        portal['marketfolder1'].invokeFactory('eisoo.market.meetapplyfolder', 'meetapplyfolder1')
        portal['marketfolder1'].invokeFactory('eisoo.market.hotelfolder', 'hotelfolder1')
        
        portal['marketfolder1']['hotelfolder1'].invokeFactory('eisoo.market.hotel', 'hotel1',
                                                              name=u"hotel1name",
                                                              )
        
        datetmp = portal['marketfolder1'].created()
        portal['marketfolder1']['meetapplyfolder1'].invokeFactory('eisoo.market.meetapply', 'meetapply1',
                                                                  name=u"meetapply1",
                                                                  meetobject="test",
                                                                  hotel=u"hotel1name",
                                                                  next_reviewer=(TEST_USER_ID,),
                                                                  number = random.randint(10000000,100000000),
                                                                  next_obj=-5,
                                                                  meetdate = datetmp,
                                                                  area="area1",  #和实例化的管辖区域一致
                                                                  
                                                                  )
                                                                                   
    def test_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_ID, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        
        page = portal.absolute_url() + '/marketfolder1/marketpreview'
        browser.open(page)
        open('/tmp/test.html', 'w').write(browser.contents)
#我申请的会议
        self.assertTrue("meetapply1" in browser.contents)
        
#我申请的礼品
        self.assertTrue("gift1" in browser.contents)
#我申请的彩页
        self.assertTrue("promotion1" in browser.contents)
#部门费用 
        self.assertTrue("3" in browser.contents) 
        self.assertTrue("15000" in browser.contents)                            
#地区拓展费用 
        self.assertTrue("爱数" in browser.contents) 
        self.assertTrue("1000.0" in browser.contents) 