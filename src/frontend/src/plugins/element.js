import Vue from 'vue'

import {
  Link,
  Upload,
  Progress,
  Autocomplete,
  Input,
  Button,
  Form,
  FormItem,
  Message,
  Table,
  Select,
  Option,
  TableColumn,
  Dropdown,
  DropdownMenu,
  DropdownItem,
  Pagination,
  Tabs,
  TabPane,
  Dialog,
  Badge,
  Tag,
  Avatar,
  Image,
  Steps,
  Step,
  Divider,
  Collapse,
  CollapseItem,
  Row,
  Col,
  Tooltip,
  Popover,
  RadioGroup,
  Radio,
  Container,
  Footer,
  Main,
  Cascader,
  Notification,
  TimePicker,
  DatePicker,
  TimeSelect,
  MessageBox
} from 'element-ui'

Vue.use(Progress)
Vue.use(Link)
Vue.use(Autocomplete)
Vue.use(Input)
Vue.use(Button)
Vue.use(Select)
Vue.use(Option)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.use(Pagination)
Vue.use(Tabs)
Vue.use(TabPane)
Vue.use(Dialog)
Vue.use(Badge)
Vue.use(Upload)
Vue.use(Tag)
Vue.use(Image)
Vue.use(Avatar)
Vue.use(Steps)
Vue.use(Step)
Vue.use(Upload)
Vue.use(Divider)
Vue.use(Input)
Vue.use(Collapse)
Vue.use(CollapseItem)
Vue.use(Row)
Vue.use(Col)
Vue.use(Tooltip)
Vue.use(Popover)
Vue.use(RadioGroup)
Vue.use(Radio)
Vue.use(Container)
Vue.use(Footer)
Vue.use(Main)
Vue.use(Cascader)
Vue.use(TimePicker)
Vue.use(DatePicker)
Vue.use(TimeSelect)
Vue.component(MessageBox)
Vue.component(Message)
Vue.prototype.$ELEMENT = {
  size: 'small',
  zIndex: 2000
}
Vue.prototype.$msgbox = MessageBox
Vue.prototype.$alert = MessageBox.alert
Vue.prototype.$confirm = MessageBox.confirm
Vue.prototype.$prompt = MessageBox.prompt
Vue.prototype.$message = Message
Vue.prototype.$notify = Notification
