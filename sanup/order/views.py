import json

from django.contrib.auth.decorators import login_required
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.models import Company
from design_data.models import *
from order.models import Order, Order_DesignData
from account.models import Account
import datetime
from django.utils import timezone
from rest_framework import viewsets
from .serializer import *




# order 등록수정해야 할점 시간이 무조건 15:00 로 들어감. html order_date 를 disabled 하고 현재시간으로 세팅하는게 바람직해보임.

@login_required(login_url='/')
def order(request):

    title = 'Order'
    '''
    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'ApiKey': '4eeca0624bd04dbba644963e2819b89c'
    }
    #주문자 연계 시스템 스타일 오더정보
    jsonData = requests.get("http://api.lookiss.com:9403/api/SCC/GetStyleFabrics", headers=headers)
    data = json.loads(jsonData.text)
    try:
        for styleObj in data:
            for obj in styleObj['fabrics']:
                st_fairic = Style_fabric.objects.create(fabric_code=obj['fabricCode'], fabric_name=obj['fabricName'],
                             fabric_color=obj['fabricColor'], fabric_size=obj['fabricSize'],
                             fabric_part=obj['fabricPart'], fabric_Construction=obj['fabricConstruction'],
                             fabric_width=obj['fabricWidth'], cuttable_width=obj['cuttableWidth'],
                             sMeter_width=obj['sMeterWeight'], yard_weight=obj['yardWeight'], unit=obj['unit'],
                             fabric_Csm=obj['fabricCsm'],
                             fabric_Mrp=obj['fabricMrp'], dyeProcessTypeCode=obj['dyeProcessTypeCode'],
                             dyeProcessTypeName=obj['dyeProcessTypeName'], dyeCompanyName=obj['dyeCompanyName'],
                             knitCompanyName=obj['knitCompanyName'])
                st_fairic.save()
                if obj['yarns'] != '':
                    for yarn_obj in obj['yarns']:
                        style_fabric = Style_fabric.objects.get(fabric_code=obj['fabricCode'])
                        st_yarn = Style_yarn.objects.create(st_yarn_code=yarn_obj['yarnCode'], st_yarn_name=yarn_obj['yarnName'], st_yarn_color=yarn_obj['yarnColor'], st_yarn_rate=yarn_obj['contentRate'],
                                   st_yarn_cnt=yarn_obj['yarnCount'], yn_Dye=yarn_obj['ynDye'])
                        st_yarn.save()
                        style_fabric.yarn = st_yarn
                        style_fabric.save()
    except Exception as e:
        print(e)
        pass
    '''
    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'ApiKey': '4eeca0624bd04dbba644963e2819b89c'
    }
    jsonData = requests.get("http://api.lookiss.com:9403/api/SCC/GetKnitWorks", headers=headers)
    data = json.loads(jsonData.text)
    try:
        for orderObj in data:
            print(orderObj)
    except Exception as e:
        print(e)
        pass
    '''
    headers = {
        'Content-Type': "multipart/form-data",
        'ApiKey': '4eeca0624bd04dbba644963e2819b89c'
    }
    data = {
               "KnitOutKey":"06f73048-2dab-46bd-97f3-52a77615088e",
      "KnitWorkKey":"",
      "OutDate":"2020-10-19",
      "SupplierCode":"4eeca0624bd04dbba644963e2819b89c",
      "SupplierName":"(주)영우시엔아이",
      "CustomerCode":"85428c333d6b45c6a5a1a01e42683bc7",
      "CustomerName":"(주)보강시스템",
      "CustomerUser":"홍길동",
      "CustomerTel":"",
      "CustomerAddress":"",
      "RollCount":1,
      "Remark":"",
      "Items":[
         {
            "StyleKey":"27e19c46-9ba1-4fa7-b4fa-0153ba97e685",
            "FabricCode":"NYPU2K2002",
            "FabricName":"파워넷 PN-2140",
            "FabricColor":"BK",
            "FabricSize":"60 / 58",
            "Unit":"M",
            "RollNo":"1",
            "OutQty":50.0000
         }
      ]
    }
    try:
        datasend = requests.post('http://api.lookiss.com:9403/api/SCC/ChangeWorkStatus', headers=headers, data=data)
        print(datasend)
    except Exception as e:
        print(e)
    '''
    myCompany = Company.objects.get(id=1)
    if request.method == 'POST':
        company = request.POST['company']
        buyer = request.POST['buyer']
        #username = request.POST['username']
        #order_date_str = request.POST['order_date']
        order_type = request.POST['order_type']
        order_inout = request.POST['order_inout']
        order_round = request.POST['order_round']
        due_date_str = request.POST['due_date']
        designQty = request.POST.getlist('designQty')
        designID = request.POST.getlist('designID')

        #print(order_date_str)
        # html input type=date 를 받아오면 문자열로 받아옴. date 로 변환
        #order_date = datetime.datetime.strptime(order_date_str, '%Y-%m-%d').date()

        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        order_date = timezone.localtime()



        #Updated upstream
        # 오더코드 = 현재시간 + 오더타입 + 오더인아웃
        order_code = datetime.datetime.today().strftime("%Y%m%d%H%M%S")[2:] + str(order_type) + str(order_inout)
        # 오덬코드 = 현재시간(-20) + 오더타입 + 오더인아웃 + 차수
        #order_code = datetime.datetime.today().strftime("%Y%m%d%H%M%S")[2:] + str(order_type) + str(order_inout) + str(order_round)

        order = Order(company=company, manager=request.user, code=order_code, buyer=buyer, type=order_type, state=0, order_date=order_date, due_date=due_date, order_inout=order_inout, order_round=order_round)
        order.save()

        # 오더 디자인데이터 저장
        for i in range(len(designID)):
            design_data = FSTY_CAD_Design_Data(CAD_Design_Data_id=int(designID[i]))
            designOrder = Order_DesignData(order_id=order, code=order_code+"-"+str(i+1), design_data_id=design_data, design_qty=int(designQty[i]))
            designOrder.save()

        return redirect('/order')

    orderList = Order.objects.all().order_by('-id')
    designList = FSTY_CAD_Design_Data.objects.all().order_by("-CAD_Design_Data_id")
    accountList = Account.objects.all()
    style_order = Style_order.objects.all()

    return render(request, 'order.html', {'title':title, 'designCount':designList.count(), 'orderCount':orderList.count(),
                                          'designDataList': designList, 'orderList': orderList, 'company': myCompany.name,
                                          'accountList':accountList,'userlang':request.user,'style_order':style_order})

@csrf_exempt
def ordercheack(request):

    if request.method == 'POST':

        oid = request.POST['oid']
        ordercheack = True
        order = Order.objects.get(id=oid)
        order.cheack = ordercheack
        order.save()

        return render(request, 'order.html', {})

@csrf_exempt
def getOrderListByJson(request):
    jsonOrderList = []
    orderList = Order.objects.all()

    for orderObj in orderList:
        jsonOrderObj = {}
        jsonOrderObj['orderId'] = orderObj.id
        jsonOrderObj['company'] = orderObj.company
        jsonOrderObj['manager'] = orderObj.manager.name
        jsonOrderObj['code'] = orderObj.code
        jsonOrderObj['buyer'] = orderObj.buyer
        jsonOrderObj['type'] = orderObj.type
        jsonOrderObj['state'] = orderObj.state
        jsonOrderObj['order_date'] = orderObj.order_date.strftime("%Y-%m-%d")
        jsonOrderObj['due_date'] = orderObj.due_date.strftime("%Y-%m-%d")
        jsonOrderObj['order_round'] = orderObj.order_round
        jsonOrderObj['order_inout'] = orderObj.order_inout

        jsonOrderList.append(jsonOrderObj)

    return HttpResponse(json.dumps({'orderList': jsonOrderList}), content_type='application/json')
    return HttpResponse(json.dumps({}), content_type='application.json')
@csrf_exempt
def showQr(request, id):
    return render(request, 'showQr.html', {'id':id})

@csrf_exempt
def getSubOrderByJson(request, id):
    subOrderObj = Order_DesignData.objects.get(id=id)
    jsonSubOrderObj = {}
    jsonSubOrderObj['code'] = subOrderObj.code
    jsonSubOrderObj['design_qty'] = subOrderObj.design_qty
    if subOrderObj.qr_code == '' or subOrderObj.qr_code == None:
        jsonSubOrderObj['qr_code'] = None
    else:
        jsonSubOrderObj['qr_code'] = subOrderObj.qr_code.url

    jsonDesignObj = {}

    layerList = FSTY_CAD_Layer.objects.filter(CAD_Layer_design_data=subOrderObj.design_data_id)
    fabricList = FSTY_CAD_Fabric.objects.filter(CAD_Fabric_production=subOrderObj.design_data_id.fsty_cad_production)

    jsonFabricList = []
    for fabricObj in fabricList:
        jsonFabricObj = {}
        jsonFabricObj['Fabric_id'] = fabricObj.CAD_Fabric_id
        jsonFabricObj['Fabric_type'] = fabricObj.CAD_Fabric_type
        jsonFabricObj['Fabric_wpi'] = fabricObj.CAD_Fabric_wpi
        jsonFabricObj['Fabric_cpi'] = fabricObj.CAD_Fabric_cpi
        jsonFabricObj['Fabric_width'] = fabricObj.CAD_Fabric_width
        jsonFabricObj['Fabric_weight_per_width'] = fabricObj.CAD_Fabric_weight_per_width
        jsonFabricList.append(jsonFabricObj)

    jsonLayerList = []
    for layerObj in layerList:
        jsonLayerObj = {}
        jsonLayerObj['Layer_id'] = layerObj.CAD_Layer_id
        jsonLayerObj['Layer_name'] = layerObj.CAD_Layer_name
        jsonLayerObj['Layer_ratio'] = layerObj.CAD_Layer_ratio
        jsonLayerObj['Layer_mm_rack'] = layerObj.CAD_Layer_mm_rack
        jsonLayerObj['Layer_use'] = layerObj.CAD_Layer_use
        jsonLayerObj['Layer_beam'] = layerObj.CAD_Layer_beam
        jsonLayerObj['Layer_total'] = layerObj.CAD_Layer_total
        jsonLayerObj['Layer_iodata'] = layerObj.CAD_Layer_iodata
        jsonLayerObj['Yarn'] = {}
        jsonLayerObj['Yarn']['id'] = layerObj.fsty_cad_yarn.CAD_Yarn_id
        jsonLayerObj['Yarn']['idx'] = layerObj.fsty_cad_yarn.CAD_Yarn_idx
        jsonLayerObj['Yarn']['maker'] = layerObj.fsty_cad_yarn.CAD_Yarn_maker
        jsonLayerObj['Yarn']['spec'] = layerObj.fsty_cad_yarn.CAD_Yarn_spec
        jsonLayerObj['Yarn']['code'] = layerObj.fsty_cad_yarn.CAD_Yarn_code
        jsonLayerObj['Yarn']['rgb_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_rgb_color
        jsonLayerObj['Yarn']['lab_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_lab_color
        jsonLayerObj['Yarn']['pantone_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_pantone_color
        jsonLayerObj['Chain_Link'] = {}
        jsonLayerObj['Chain_Link']['id'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_id
        jsonLayerObj['Chain_Link']['course'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_course
        jsonLayerList.append(jsonLayerObj)

    jsonDesignObj['Design_Data_id'] = subOrderObj.design_data_id.CAD_Design_Data_id
    jsonDesignObj['Design_Data_name'] = subOrderObj.design_data_id.CAD_Design_Data_name
    jsonDesignObj['Design_Data_code'] = subOrderObj.design_data_id.CAD_Design_Data_code
    jsonDesignObj['Design_Data_pattern_image'] = subOrderObj.design_data_id.CAD_Design_Data_pattern_image.url
    jsonDesignObj['Design_Data_simulation_image'] = subOrderObj.design_data_id.CAD_Design_Data_simulation_image.url
    jsonDesignObj['Design_Data_create_date'] = subOrderObj.design_data_id.CAD_Design_Data_create_date.strftime("%Y-%m-%d")
    jsonDesignObj['Design_Data_magnification'] = subOrderObj.design_data_id.CAD_Design_Data_magnification
    jsonDesignObj['Production'] = {}
    jsonDesignObj['Production']['id'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_id
    jsonDesignObj['Production']['quota_per_day'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_quota_per_day
    jsonDesignObj['Production']['machine_name'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_machine_name
    jsonDesignObj['Production']['note'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_note
    jsonDesignObj['Production']['Fabric'] = jsonFabricList
    jsonDesignObj['Layer'] = jsonLayerList

    jsonSubOrderObj['design_data'] = jsonDesignObj

    return HttpResponse(json.dumps(jsonSubOrderObj), content_type='application/json')
@csrf_exempt
def getOrderByJson(request, orderId):

    jsonOrderObj = {}

    if orderId != None:
        orderObj = Order.objects.get(id=orderId)
        jsonOrderObj['company'] = orderObj.company
        jsonOrderObj['manager'] = orderObj.manager.name
        jsonOrderObj['code'] = orderObj.code
        jsonOrderObj['buyer'] = orderObj.buyer
        jsonOrderObj['type'] = orderObj.type
        jsonOrderObj['state'] = orderObj.state
        jsonOrderObj['order_date'] = orderObj.order_date.strftime("%Y-%m-%d")
        jsonOrderObj['due_date'] = orderObj.due_date.strftime("%Y-%m-%d")
        jsonOrderObj['order_round'] = orderObj.order_round
        jsonOrderObj['order_inout'] = orderObj.order_inout

        subOrderList = Order_DesignData.objects.filter(order_id=orderObj)

        jsonSubOrderList = []

        for subOrderObj in subOrderList:
            jsonSubOrderObj = {}
            jsonSubOrderObj['code'] = subOrderObj.code
            jsonSubOrderObj['design_qty'] = subOrderObj.design_qty
            if subOrderObj.qr_code == '' or subOrderObj.qr_code == None:
                jsonSubOrderObj['qr_code'] = None
            else:
                jsonSubOrderObj['qr_code'] = subOrderObj.qr_code.url

            jsonDesignObj = {}

            layerList = FSTY_CAD_Layer.objects.filter(CAD_Layer_design_data=subOrderObj.design_data_id)
            fabricList = FSTY_CAD_Fabric.objects.filter(CAD_Fabric_production=subOrderObj.design_data_id.fsty_cad_production)

            jsonFabricList = []
            for fabricObj in fabricList:
                jsonFabricObj = {}
                jsonFabricObj['CAD_Fabric_id'] = fabricObj.CAD_Fabric_id
                jsonFabricObj['CAD_Fabric_type'] = fabricObj.CAD_Fabric_type
                jsonFabricObj['CAD_Fabric_wpi'] = fabricObj.CAD_Fabric_wpi
                jsonFabricObj['CAD_Fabric_cpi'] = fabricObj.CAD_Fabric_cpi
                jsonFabricObj['CAD_Fabric_width'] = fabricObj.CAD_Fabric_width
                jsonFabricObj['CAD_Fabric_weight_per_width'] = fabricObj.CAD_Fabric_weight_per_width
                jsonFabricList.append(jsonFabricObj)

            jsonLayerList = []
            for layerObj in layerList:
                jsonLayerObj = {}
                jsonLayerObj['CAD_Layer_id'] = layerObj.CAD_Layer_id
                jsonLayerObj['CAD_Layer_name'] = layerObj.CAD_Layer_name
                jsonLayerObj['CAD_Layer_ratio'] = layerObj.CAD_Layer_ratio
                jsonLayerObj['CAD_Layer_mm_rack'] = layerObj.CAD_Layer_mm_rack
                jsonLayerObj['CAD_Layer_use'] = layerObj.CAD_Layer_use
                jsonLayerObj['CAD_Layer_beam'] = layerObj.CAD_Layer_beam
                jsonLayerObj['CAD_Layer_total'] = layerObj.CAD_Layer_total
                jsonLayerObj['CAD_Layer_iodata'] = layerObj.CAD_Layer_iodata
                jsonLayerObj['FSTY_CAD_Yarn'] = {}
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_id'] = layerObj.fsty_cad_yarn.CAD_Yarn_id
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_idx'] = layerObj.fsty_cad_yarn.CAD_Yarn_idx
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_maker'] = layerObj.fsty_cad_yarn.CAD_Yarn_maker
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_spec'] = layerObj.fsty_cad_yarn.CAD_Yarn_spec
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_code'] = layerObj.fsty_cad_yarn.CAD_Yarn_code
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_rgb_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_rgb_color
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_lab_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_lab_color
                jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_pantone_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_pantone_color
                jsonLayerObj['FSTY_CAD_Chain_Link'] = {}
                jsonLayerObj['FSTY_CAD_Chain_Link']['CAD_Chain_Link_id'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_id
                jsonLayerObj['FSTY_CAD_Chain_Link']['CAD_Chain_Link_course'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_course
                jsonLayerList.append(jsonLayerObj)

            jsonDesignObj['CAD_Design_Data_id'] = subOrderObj.design_data_id.CAD_Design_Data_id
            jsonDesignObj['CAD_Design_Data_name'] = subOrderObj.design_data_id.CAD_Design_Data_name
            jsonDesignObj['CAD_Design_Data_code'] = subOrderObj.design_data_id.CAD_Design_Data_code
            jsonDesignObj['CAD_Design_Data_pattern_image'] = subOrderObj.design_data_id.CAD_Design_Data_pattern_image.url
            jsonDesignObj['CAD_Design_Data_simulation_image'] = subOrderObj.design_data_id.CAD_Design_Data_simulation_image.url
            jsonDesignObj['CAD_Design_Data_create_date'] = subOrderObj.design_data_id.CAD_Design_Data_create_date.strftime("%Y-%m-%d")
            jsonDesignObj['CAD_Design_Data_magnification'] = subOrderObj.design_data_id.CAD_Design_Data_magnification
            jsonDesignObj['FSTY_CAD_Production'] = {}
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_id'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_id
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_quota_per_day'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_quota_per_day
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_machine_name'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_machine_name
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_note'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_note
            jsonDesignObj['FSTY_CAD_Production']['FSTY_CAD_Fabric'] = jsonFabricList
            jsonDesignObj['FSTY_CAD_Layer'] = jsonLayerList

            jsonSubOrderObj['design_data'] = jsonDesignObj

            jsonSubOrderList.append(jsonSubOrderObj)

        jsonOrderObj['subOrder'] = jsonSubOrderList

    return HttpResponse(json.dumps({'order': jsonOrderObj}), content_type='application/json')


def modifyOrder(request):

    oid = request.POST['oid']
    buyer = request.POST['detailBuyer']
    order_date_str = request.POST['detailOrderDate']
    due_date_str = request.POST['detailDueDate']
    order_type = request.POST['detailOrderType']
    order_inout = request.POST['detailOrderInout']
    order_round = request.POST['detailRound']
    sub_order_code = int(request.POST['subOrderCode'])
    sub_design_qty = int(request.POST['subDesignQty'])


    order = Order.objects.get(id=oid)

    due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()

    order_date = datetime.datetime.strptime(order_date_str, '%Y-%m-%d').date()
    order.buyer = buyer
    order.order_Date = order_date
    order.due_date = due_date
    order.order_type = order_type
    order.order_inout = order_inout
    order.order_round = order_round

    order.save()

    designOrder = Order_DesignData.objects.get(order_id=order, code=str(order.code)+'-'+str(sub_order_code+1))
    designOrder.design_qty = sub_design_qty
    designOrder.save()

    return redirect('/order')

@csrf_exempt
def delete(request):
    oid = request.POST['orderId']
    order = Order.objects.get(id=oid)

    order.delete()

    return redirect('/order')

def warpTable(request, id):
    tablebot = []
    try:
        warptopJSON = requests.get("http://tnswebserver.iptime.org:1978/api/tws_chart").json()#1번
        warpbotJSON = requests.get("http://tnswebserver.iptime.org:1978/api/tws_chart/beam").json()#2번
        for jsontop in warptopJSON['tws_chart_']:
            if jsontop['tws_order_make_number'] == '56':
                warpTabletop = {}
                warpTabletop['yarn_name'] = jsontop["tws_order_yarn_name"]
                warpTabletop['setno'] = jsontop['tws_order_set_number']
                warpTabletop['lotno'] = jsontop['tws_order_lot_number']
                warpTabletop['bon_number'] = jsontop['tws_order_machine_nmuber']
                warpTabletop['bim_number'] = jsontop['tws_order_bm_number']
                warpTabletop['creel_speed'] = jsontop['tws_order_creel_speed']
                warpTabletop['warper_speed'] = jsontop['tws_order_warper_speed']
                warpTabletop['drift'] = jsontop['tws_order_pre_stretch']
                warpTabletop['tention'] = jsontop['tws_order_final_stretch']
        for jsonbot in warpbotJSON['warper_beam_']:
            if jsonbot['tws_order_make_number'] == '52':
                warpTablebot = {}
                warpTablebot['beam_no'] = jsonbot['warperbeam_code']
                warpTablebot['meter'] = jsonbot['tws_warper_total_length']
                warpTablebot['turn_count'] = jsonbot['tws_current_turncnt']
                warpTablebot['warp_time1'] = jsonbot['tws_time1']
                warpTablebot['warp_time2'] = jsonbot['tws_time2']
                warpTablebot['beam_circum'] = jsonbot['tws_warper_outside']
                warpTablebot['warp_manage'] = jsonbot['user_name']
                tablebot.append(warpTablebot)
    except Exception as e:
        print(e)
    variables = {'top': warpTabletop, 'bot': tablebot, 'userlang':request.user}
    return render(request, 'worksheet/warp.html', variables)


@csrf_exempt
def rawroll(request, id):
    if request.method == "GET":
        order = Order.objects.get(id=id)
        buyer = order.buyer
        order_sub = Order_DesignData.objects.get(order_id=id)
        company = Company.objects.get(id=1)
        #design_name = FSTY_CAD_Design_Data.objects.get(id=order_sub.de)

        account = Account.objects.get(accountname=buyer)
        return render(request, 'worksheet/rawroll.html', {'orderaccount':account,'order_sub':order_sub,'order':order, 'company':company})

class Order_design_data_api(viewsets.ModelViewSet):
    queryset = Order_DesignData.objects.all()
    serializer_class = Order_design_Serializer

class Order_api(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = Order_Serializer
