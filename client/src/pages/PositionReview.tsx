import {
  Input,
  Button,
  Modal,
  Form,
  type FormProps,
  DatePicker,
  message,
  List,
} from 'antd';
import './PositionReview.css';
import type { Moment } from 'moment';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  getPositionReviewApi,
  addPositionReviewApi,
  type PositionReviewItem,
} from '@/apis/api';
export default function PositionReview() {
  const [modalOpen, setModalOpen] = useState(false);
  const [list, setList] = useState<PositionReviewItem[]>([]);
  const [showData, setShowData] = useState<PositionReviewItem[]>([]);
  const [more, setMore] = useState(false);
  useEffect(() => {
    getPositionReviewApi().then((res) => {
      if (res && res.data) {
        setList(res.data);
        setShowData(res.data.slice(0, 10));
        setMore(res.data.length > 10);
      }
    });
  }, []);
  const onSearch = () => {};
  return (
    <div className="relative w100p h100p overflow-hidden">
      <Button
        type="primary"
        className="rs-add-button"
        onClick={() => setModalOpen(true)}
      >
        新增领悟
      </Button>
      <ReflectSelectionModal
        modalOpen={modalOpen}
        setModalOpen={setModalOpen}
      />
      <div className="rs-search-area">
        <Input.Search
          placeholder="输入问题"
          allowClear
          enterButton="Search"
          size="large"
          onSearch={onSearch}
        />
        <List
          size="large"
          footer={more ? <div>show more</div> : null}
          bordered
          dataSource={showData}
          renderItem={(item) => (
            <List.Item>
              <Link to={'/rs/' + item.id}>{item.title}</Link>
            </List.Item>
          )}
        />
      </div>
    </div>
  );
}

interface ReflectSelectionModalProps {
  modalOpen: boolean;
  setModalOpen: (val: boolean) => void;
}
type FieldType = {
  title: string;
  code: string;
  date: Moment;
  description: string;
};
const ReflectSelectionModal = ({
  modalOpen,
  setModalOpen,
}: ReflectSelectionModalProps) => {
  const [messageApi, contextHolder] = message.useMessage();
  const onFinish: FormProps<FieldType>['onFinish'] = (values) => {
    let date = values.date.format('YYYY-MM-DD') + ' 15:00:00';
    date = new Date(date).getTime().toString();
    addPositionReviewApi(
      values.code,
      values.title,
      date,
      values.description,
    ).then((res) => {
      if (res.data) {
        messageApi.success('成功');
        setModalOpen(false);
      } else {
        messageApi.error('添加失败');
      }
    });
  };
  return (
    <>
      {contextHolder}
      <Modal
        title="新增感悟"
        footer={null}
        open={modalOpen}
        onCancel={() => setModalOpen(false)}
      >
        <Form
          name="basic"
          labelCol={{ span: 4 }}
          wrapperCol={{ span: 20 }}
          style={{ maxWidth: 1000 }}
          initialValues={{ remember: true }}
          onFinish={onFinish}
          autoComplete="off"
        >
          <Form.Item<FieldType>
            label="标题"
            name="title"
            rules={[{ required: true, message: '请输入标题!' }]}
          >
            <Input />
          </Form.Item>

          <Form.Item<FieldType>
            label="股票代码"
            name="code"
            rules={[{ required: true, message: '请输入股票代码!' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item<FieldType>
            label="日期"
            name="date"
            rules={[{ required: true, message: '请选择日期!' }]}
          >
            <DatePicker format="YYYY-MM-DD" />
          </Form.Item>

          <Form.Item<FieldType>
            label="详细"
            name="description"
            rules={[{ required: true, message: '请输入详细解析!' }]}
          >
            <Input.TextArea rows={10} />
          </Form.Item>

          <Form.Item label={null}>
            <Button type="primary" htmlType="submit">
              提交
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};
