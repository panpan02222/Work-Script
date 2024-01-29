/*
 Navicat Premium Data Transfer

 Source Server         : 105
 Source Server Type    : MySQL
 Source Server Version : 80034
 Source Host           : 192.162.1.105:3306
 Source Schema         : text2sql

 Target Server Type    : MySQL
 Target Server Version : 80034
 File Encoding         : 65001

 Date: 25/09/2023 19:55:44
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for STOCK
-- ----------------------------
DROP TABLE IF EXISTS `Test_Table_01`;
CREATE TABLE `Test_Table_01`  (
  `STOCK_ID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '库存批次号，对库存业务数据标准表进行定义的主键，用以唯一标识模型，也可用于与其他模型进行关联',
  `PROV_ORG_NAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '省公司名称，发生订单操作、出入库等业务的所属省公司编码，如“10-国网江苏省电力有限公司”，用于国网总部分析各省公司入库业务',
  `CITY_NAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '地市公司名称，发生订单处理、出入库等业务所属地市公司或直属单位名称，如“国网江苏省电力有限公司南京供电公司”、“国网江苏电力有限公司建设分公司”，用于省公司分析各市公司或直属单位库存移动业务',
  `STORAGE_NAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '库存地点名称，物料库存移动时的目标库存地点编码对应的仓库名称：“国网南京供电公司石门坎仓库”',
  `MEAS_UNIT_TYPE` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '计量单位，物料编码自动带出的计量单位编码，指明采购申请行项目对应的计量单位。',
  `MATERIAL_NAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '物资名称，物资大类来源于（MDM）系统，属于物资主数据的最粗颗粒度的归类层级，包括一次设备、二次设备、低压电器等分类描述，用于作为采购物资大类名称的唯一识别码对应的文本简述，例如：采购申请阶段，在ERP系统中，系统根据物料编码自动关联对应的物料大类名称，物资一级分类描述。',
  `STOCK_NUMBER` int(0) NOT NULL COMMENT '库存数量，已冻结的库存物资的数量，不可直接领料或调拨，需要通过将冻结库存转换成非限制库存方可直接领料或调拨。',
  `PROJECT_NAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '项目名称，由需求计划提报人员维护的大工程项目名称，采购申请行项目对应的工程项目名称，如需求计划申报阶段，在ERP系统中，是大工程名称，“国网舟山供电公司2021年桃花供电所业务外包委托服务”，用于作为工程项目名称的唯一识别码对应的文本简述',
  `SUPPLIER_NAME` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '供应商名称，供应商是指直接向国网公司提供商品或服务的企业。供应商名称为企业的全称。由ECP2.0等系统同步至MDM系统的信息，或操作人在MDM系统中创建供应商时维护的信息，在不同场景代表不同的角色，如投标人、中标人、合同卖方等',
  `GODENTRY_POSTING_DATE` datetime(0) NOT NULL COMMENT '入库单过账日期，业务人员在系统中操作物料凭证时，系统默认或由业务人员手工选择的过账日期，如“2021-01-02”，在实际业务中可将该日期作为物料的实际入库日期。一般用过账日期作为入库业务统计分析的时间维度',
  PRIMARY KEY (`STOCK_ID`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
