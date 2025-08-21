import React, { useState, useEffect } from 'react';
import { Button, Flex, Table } from 'antd';
import type { TableColumnsType, TableProps } from 'antd';
import {
  getSelectionApi,
  addSelectionApi,
  deleteSelectionApi,
  type SelectionItem,
} from '@/apis/api';

type TableRowSelection<T extends object = object> =
  TableProps<T>['rowSelection'];

const columns: TableColumnsType<DataType> = [
  { title: '代码', dataIndex: 'code' },
  { title: '名称', dataIndex: 'name' },
  { title: '涨幅', dataIndex: 'increase' },
  { title: '价格', dataIndex: 'price' },
];

const dataSource: DataType[] = [];

const App: React.FC = () => {
  const [data, setData] = useState<SelectionItem[]>([]);
  useEffect(() => {
    // 获取自选列表
    getSelectionApi().then((response) => {
      if (response && response.data) {
        setData(response.data);
      }
    });
  }, []);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);

  const addSelection = () => {};

  const onSelectChange = (newSelectedRowKeys: React.Key[]) => {
    console.log('selectedRowKeys changed: ', newSelectedRowKeys);
    setSelectedRowKeys(newSelectedRowKeys);
  };

  const rowSelection: TableRowSelection<DataType> = {
    selectedRowKeys,
    onChange: onSelectChange,
  };

  const hasSelected = selectedRowKeys.length > 0;

  return (
    <Flex gap="middle" vertical>
      <Flex align="center" gap="middle">
        <Button type="primary" onClick={addSelection}>
          添加自选
        </Button>
        {hasSelected ? `Selected ${selectedRowKeys.length} items` : null}
      </Flex>
      <Table<DataType>
        rowSelection={rowSelection}
        columns={columns}
        dataSource={dataSource}
      />
    </Flex>
  );
};

export default App;
